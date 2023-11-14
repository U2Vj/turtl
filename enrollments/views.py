import re

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Task, Regex, Flag, QuestionChoice, Question
from .models import Enrollment, TaskSolution
from .serializers import EnrollmentSerializer, EnrollmentDetailSerializer, TaskSolutionSerializer


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


class TaskSolutionVerificationView(ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = TaskSolutionSerializer

    def create(self, request, *args, **kwargs):
        enrollment_id = kwargs.get('enrollment_id')
        task_id = kwargs.get('task_id')

        # Verify that the enrollment and task exist
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, student=request.user)
            task = Task.objects.get(id=task_id, project__classroom=enrollment.classroom)
        except Enrollment.DoesNotExist:
            raise NotFound('Enrollment not found.')
        except Task.DoesNotExist:
            raise NotFound('Task not found.')

        # Extract solutions from request
        regex_solutions = {item['id']: item for item in request.data.get('regexes', [])}
        flag_solutions = {item['id']: item for item in request.data.get('flags', [])}
        question_solutions = request.data.get('questions', [])

        response_data = {
            "regexes": {},
            "flags": {},
            "questions": {},
            "passed": False,
            "first_time_passed": False,
        }

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

        # Prepare a dictionary for questions and their correct choices
        questions_by_id = {
            question.id: set(
                QuestionChoice.objects.filter(question=question, is_correct=True).values_list('id', flat=True)
            ) for question in task.acceptance_criteria.questions.all()
        }

        # Check if all questions are submitted
        if len(question_solutions) != len(questions_by_id):
            response_data["questions"] = {question_id: "missing" for question_id in questions_by_id.keys()}
            task_passed = False

        # Verify Question Solutions
        for solution in question_solutions:
            correct_choices = questions_by_id.get(solution['id'])
            submitted_choices = set(solution['selected_choices'])
            if correct_choices:
                is_correct = submitted_choices == correct_choices
                response_type = "correct" if is_correct else "incorrect"
                response_data["questions"][solution['id']] = response_type
                if not is_correct:
                    task_passed = False
            else:
                response_data["questions"][solution['id']] = "not found"
                task_passed = False

        # If passed for the first time, create a new TaskSolution
        first_time_passed = task_passed and not TaskSolution.objects.filter(enrollment=enrollment, task=task).exists()
        if first_time_passed:
            TaskSolution.objects.create(enrollment=enrollment, task=task)

        response_data["passed"] = task_passed
        response_data["first_time_passed"] = first_time_passed
        return Response(response_data, status=status.HTTP_200_OK)
