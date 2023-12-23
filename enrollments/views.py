import re

from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom
from catalog.models import Task, QuestionChoice
from catalog.predicates import manages_classroom
from .models import Enrollment
from .models import TaskSolution
from .serializers import EnrollmentSerializer, EnrollmentDetailSerializer, EnrollmentUserSerializer, \
    TaskSubmissionSerializer


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
    permission_classes = (IsAuthenticated,)
    queryset = Enrollment.objects.all()


class ClassroomEnrollmentListView(ModelViewSet):
    serializer_class = EnrollmentUserSerializer
    permission_classes = (IsAuthenticated,)

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


class TaskSubmissionView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSubmissionSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

    @staticmethod
    def _verify_regexes(task: Task, regex_submission, regex_response):
        regexes_valid = True
        for regex in task.acceptance_criteria.regexes.all():
            submission = regex_submission.get(regex.id)
            print(regex.pattern)
            if submission:
                print(re.match(regex.pattern, submission['solution']))
                if re.match(regex.pattern, submission['solution']):
                    regex_response[regex.id] = "correct"
                else:
                    regex_response[regex.id] = "incorrect"
                    regexes_valid = False
            else:
                regex_response[regex.id] = "missing"
                regexes_valid = False
        return regexes_valid

    @staticmethod
    def _verify_flags(task: Task, flag_submission, flag_response):
        flags_valid = True
        for flag in task.acceptance_criteria.flags.all():
            submission = flag_submission.get(flag.id)
            if submission:
                if flag.value == submission['solution']:
                    flag_response[flag.id] = "correct"
                else:
                    flag_response[flag.id] = "incorrect"
                    flags_valid = False
            else:
                flag_response[flag.id] = "missing"
                flags_valid = False
        return flags_valid

    @staticmethod
    def _verify_questions(task: Task, question_submission, question_response):
        questions_with_choices = task.acceptance_criteria.questions.all().prefetch_related(
            # Prefetch the correct choices to avoid a query for each question
            Prefetch('choices', queryset=QuestionChoice.objects.filter(is_correct=True),
                     to_attr='correct_choices')
        )
        questions_valid = True
        for question in questions_with_choices:
            submission = question_submission.get(question.id)
            if submission:
                selected_choices = set(submission['selected_choices'])
                correct_choices = set(choice.id for choice in question.correct_choices)
                if selected_choices == correct_choices:
                    question_response[question.id] = "correct"
                else:
                    question_response[question.id] = "incorrect"
                    questions_valid = False
            else:
                question_response[question.id] = "missing"
                questions_valid = False
        return questions_valid

    def post(self, request, enrollment_id: int, *args, **kwargs):
        task = self.get_object()
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        if not task.project.classroom == enrollment.classroom:
            raise ValidationError("You were trying to submit a solution for a task that is not a part of the "
                                  "enrollment's classroom.")
        if not enrollment.student == request.user:
            raise PermissionDenied

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Each line constructs a dictionary with each item's ID as the key and the item itself as the value
        regex_submission = {item['id']: item for item in serializer.validated_data['regexes']}
        flag_submission = {item['id']: item for item in serializer.validated_data['flags']}
        question_submission = {item['id']: item for item in serializer.validated_data['questions']}

        response_data = {
            "regexes": {},
            "flags": {},
            "questions": {},
            "passed": False
        }

        regexes_valid = self._verify_regexes(task, regex_submission, response_data["regexes"])
        flags_valid = self._verify_flags(task, flag_submission, response_data["flags"])
        questions_valid = self._verify_questions(task, question_submission, response_data["questions"])

        response_data["passed"] = regexes_valid and flags_valid and questions_valid

        status_code = status.HTTP_200_OK
        if response_data["passed"]:
            _, created = TaskSolution.objects.get_or_create(enrollment=enrollment, task=task)
            if created:
                status_code = status.HTTP_201_CREATED
        return Response(response_data, status=status_code)
