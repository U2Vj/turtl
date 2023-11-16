import re

from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom, Question
from catalog.models import Task, QuestionChoice
from catalog.predicates import manages_classroom
from .models import Enrollment
from .models import TaskSolution
from .serializers import EnrollmentSerializer, EnrollmentDetailSerializer, EnrollmentUserSerializer, \
    QuestionSubmissionSerializer, FlagSubmissionSerializer, RegexSubmissionSerializer
from .serializers import TaskSolutionSerializer


class EnrollmentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class EnrollmentDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = EnrollmentDetailSerializer
    queryset = Enrollment.objects.all()


class ClassroomEnrollmentListView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EnrollmentUserSerializer

    @action(detail=False, methods=['get'], url_path='for-classroom')
    def list_enrollments(self, request, pk=None):
        classroom = get_object_or_404(Classroom, pk=pk)

        if not request.user.is_administrator:
            if not request.user.is_instructor:
                return Response({"detail": "Access denied: User is not an instructor."},
                                status=status.HTTP_403_FORBIDDEN)
            if not manages_classroom(request.user, classroom):
                return Response({"detail": "Access denied: User does not manage this classroom."},
                                status=status.HTTP_403_FORBIDDEN)
        queryset = Enrollment.objects.filter(classroom=classroom)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskSubmissionView(ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = TaskSolutionSerializer

    @staticmethod
    def verify_submissions(task, regex_submission, flag_submission, question_submission,
                           regex_response, flag_response, question_response):
        task_passed = True
        task_passed &= TaskSubmissionView.verify_regexes(task, regex_submission, regex_response)
        task_passed &= TaskSubmissionView.verify_flags(task, flag_submission, flag_response)
        task_passed &= TaskSubmissionView.verify_questions(task, question_submission, question_response)
        return task_passed

    @staticmethod
    def verify_regexes(task, regex_submission, regex_response):
        task_passed = True
        for regex in task.acceptance_criteria.regexes.all():
            submission = regex_submission.get(regex.id)
            if submission:
                if re.match(regex.pattern, submission['solution']):
                    regex_response[regex.id] = "correct"
                else:
                    regex_response[regex.id] = "incorrect"
                    task_passed = False
            else:
                regex_response[regex.id] = "missing"
                task_passed = False
        return task_passed

    @staticmethod
    def verify_flags(task, flag_submission, flag_response):
        task_passed = True
        for flag in task.acceptance_criteria.flags.all():
            submission = flag_submission.get(flag.id)
            if submission:
                if flag.value == submission['solution']:
                    flag_response[flag.id] = "correct"
                else:
                    flag_response[flag.id] = "incorrect"
                    task_passed = False
            else:
                flag_response[flag.id] = "missing"
                task_passed = False
        return task_passed

    @staticmethod
    def verify_questions(task, question_submission, question_response):
        task_passed = True
        questions_with_choices = task.acceptance_criteria.questions.all().prefetch_related(
            # Prefetching the correct choices to avoid a query for each question
            Prefetch('choices', queryset=QuestionChoice.objects.filter(is_correct=True), to_attr='correct_choices')
        )
        for question in questions_with_choices:
            submission = question_submission.get(question.id)
            if submission:
                selected_choices = set(submission['selected_choices'])
                correct_choices = set(choice.id for choice in question.correct_choices)
                if selected_choices == correct_choices:
                    question_response[question.id] = "correct"
                else:
                    question_response[question.id] = "incorrect"
                    task_passed = False
            else:
                question_response[question.id] = "missing"
                task_passed = False
        return task_passed

    @staticmethod
    def deserialize_solutions(request):
        regex_serializer = RegexSubmissionSerializer(data=request.data.get('regexes', []), many=True)
        flag_serializer = FlagSubmissionSerializer(data=request.data.get('flags', []), many=True)
        question_serializer = QuestionSubmissionSerializer(data=request.data.get('questions', []), many=True)

        valid_regex = regex_serializer.is_valid()
        valid_flag = flag_serializer.is_valid()
        valid_question = question_serializer.is_valid()

        if not (valid_regex and valid_flag and valid_question):
            errors = {
                'regex_errors': regex_serializer.errors,
                'flag_errors': flag_serializer.errors,
                'question_errors': question_serializer.errors
            }
            raise ValidationError(errors)

        regex_submission = {item['id']: item for item in regex_serializer.validated_data}
        flag_submission = {item['id']: item for item in flag_serializer.validated_data}
        question_submission = {item['id']: item for item in question_serializer.validated_data}
        return regex_submission, flag_submission, question_submission

    @staticmethod
    def get_enrollment_and_task(enrollment_id, task_id, user):
        try:
            # Ensuring that the enrollment belongs to the current user
            enrollment = Enrollment.objects.get(id=enrollment_id, student=user)
            # Ensuring that the task is part of the enrollment classroom
            task = Task.objects.get(id=task_id, project__classroom=enrollment.classroom)
            return enrollment, task
        except Enrollment.DoesNotExist:
            raise NotFound('Enrollment not found.')
        except Task.DoesNotExist:
            raise NotFound('Task not found.')

    def create(self, request, *args, **kwargs):
        enrollment_id = kwargs.get('enrollment_id')
        task_id = kwargs.get('task_id')

        enrollment, task = TaskSubmissionView.get_enrollment_and_task(enrollment_id, task_id, request.user)
        regex_submission, flag_submission, question_submission = TaskSubmissionView.deserialize_solutions(request)

        response_data = {
            "regexes": {},
            "flags": {},
            "questions": {},
            "passed": False,
        }

        response_data["passed"] = TaskSubmissionView.verify_submissions(
            task, regex_submission, flag_submission, question_submission,
            response_data["regexes"], response_data["flags"], response_data["questions"]
        )

        if response_data["passed"] and not TaskSolution.objects.filter(enrollment=enrollment, task=task).exists():
            TaskSolution.objects.create(enrollment=enrollment, task=task)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_200_OK)
