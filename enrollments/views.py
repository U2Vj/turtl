import re

from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
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
    QuestionSolutionSerializer, FlagSolutionSerializer, RegexSolutionSerializer
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


def verify_solutions(response_data, task, regex_solutions, flag_solutions, question_solutions):
    task_passed = True

    # Verify Regex Solutions
    for regex in task.acceptance_criteria.regexes.all():
        solution = regex_solutions.get(regex.id)
        if solution:
            if re.match(regex.pattern, solution['solution']):
                response_data["regexes"][regex.id] = "correct"
            else:
                response_data["regexes"][regex.id] = "incorrect"
                task_passed = False
        else:
            response_data["regexes"][regex.id] = "missing"
            task_passed = False

    # Verify Flag Solutions
    for flag in task.acceptance_criteria.flags.all():
        solution = flag_solutions.get(flag.id)
        if solution:
            if flag.value == solution['solution']:
                response_data["flags"][flag.id] = "correct"
            else:
                response_data["flags"][flag.id] = "incorrect"
                task_passed = False
        else:
            response_data["flags"][flag.id] = "missing"
            task_passed = False

    # Efficiently fetch question choices
    questions_with_choices = task.acceptance_criteria.questions.all().prefetch_related(
        Prefetch('choices', queryset=QuestionChoice.objects.filter(is_correct=True), to_attr='correct_choices')
    )

    # Prepare a dictionary for questions and their correct choices
    questions_by_id = {
        question.id: set(choice.id for choice in question.correct_choices) for question in questions_with_choices
    }

    # Verify Question Solutions
    for question_id, correct_choices in questions_by_id.items():
        solution = question_solutions.get(question_id)
        if solution:
            submitted_choices = set(solution['selected_choices'])
            if submitted_choices == correct_choices:
                response_data["questions"][question_id] = "correct"
            else:
                response_data["questions"][question_id] = "incorrect"
                task_passed = False
        else:
            response_data["questions"][question_id] = "missing"
            task_passed = False

    return task_passed


def check_first_time_passed(enrollment, task):
    first_time_passed = not TaskSolution.objects.filter(enrollment=enrollment, task=task).exists()
    if first_time_passed:
        TaskSolution.objects.create(enrollment=enrollment, task=task)
    return first_time_passed


def deserialize_solutions(request):
    regex_serializer = RegexSolutionSerializer(data=request.data.get('regexes', []), many=True)
    flag_serializer = FlagSolutionSerializer(data=request.data.get('flags', []), many=True)
    question_serializer = QuestionSolutionSerializer(data=request.data.get('questions', []), many=True)

    if not (regex_serializer.is_valid() and flag_serializer.is_valid() and question_serializer.is_valid()):
        errors = {
            'regex_errors': regex_serializer.errors,
            'flag_errors': flag_serializer.errors,
            'question_errors': question_serializer.errors
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    regex_solutions = {item['id']: item for item in regex_serializer.validated_data}
    flag_solutions = {item['id']: item for item in flag_serializer.validated_data}
    question_solutions = {item['id']: item for item in question_serializer.validated_data}

    return regex_solutions, flag_solutions, question_solutions


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


class TaskSolutionVerificationView(ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = TaskSolutionSerializer

    def create(self, request, *args, **kwargs):
        enrollment_id = kwargs.get('enrollment_id')
        task_id = kwargs.get('task_id')

        enrollment, task = get_enrollment_and_task(enrollment_id, task_id, request.user)
        regex_solutions, flag_solutions, question_solutions = deserialize_solutions(request)

        response_data = {
            "regexes": {},
            "flags": {},
            "questions": {},
            "passed": False,
            "first_time_passed": False,
        }

        response_data["passed"] = (
            verify_solutions(response_data, task, regex_solutions, flag_solutions, question_solutions)
        )
        response_data["first_time_passed"] = response_data["passed"] and check_first_time_passed(enrollment, task)

        return Response(response_data, status=status.HTTP_200_OK)
