from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authentication.models import User
from catalog.models import Classroom, ClassroomInstructor, Project, Task, AcceptanceCriteria
from enrollments.models import Enrollment
from .models import (
    Network,
    VMTemplate,
    NetworkTemplate,
    TaskVMConfiguration,
    TaskVMTemplate,
    LabEnvironment,
    VirtualMachine,
)
from .access import user_can_access_task_vm


class VMManagerModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Basic user and catalog setup
        cls.user = User.objects.create_student("student@example.com", "password123")

        classroom = Classroom.objects.create(title="Test Classroom")
        project = Project.objects.create(title="Test Project", classroom=classroom)
        acceptance = AcceptanceCriteria.objects.create()

        cls.task = Task.objects.create(
            title="Test Task",
            project=project,
            description="Test description",
            task_type=Task.TaskType.NEUTRAL,
            difficulty=Task.Difficulty.BEGINNER,
            acceptance_criteria=acceptance,
        )

        cls.network_template = NetworkTemplate.objects.create(
            name="Test Network Template",
            subnet="10.0.0.0/24",
            vlan_id=100,
            description="Test network template",
        )

        cls.vm_template = VMTemplate.objects.create(
            name="Test VM Template",
            template_id=1,
            description="Base VM template",
            cpu_cores=2,
            memory_mb=1024,
            purpose="USER_SHELL",
        )

        cls.task_config = TaskVMConfiguration.objects.create(
            task=cls.task,
            network_template=cls.network_template,
            allow_internet_access=True,
            max_runtime_hours=24,
            auto_cleanup_after_hours=72,
        )

        cls.task_vm_template = TaskVMTemplate.objects.create(
            configuration=cls.task_config,
            template=cls.vm_template,
            planned_ip_address="10.0.0.10",
        )

        cls.network = Network.objects.create(
            name="User Network",
            subnet="10.0.0.0/24",
            vlan_id=200,
            template=cls.network_template,
            user=cls.user,
            task=cls.task,
        )

        cls.lab_environment = LabEnvironment.objects.create(
            user=cls.user,
            task=cls.task,
            network=cls.network,
        )

        cls.virtual_machine = VirtualMachine.objects.create(
            vmid=1000,
            lab_environment=cls.lab_environment,
            template=cls.vm_template,
            name="Primary VM",
            network=cls.network,
        )

    def test_network_str_representation(self):
        expected = f"{self.network.name} ({self.network.subnet}) for {self.user} in {self.task}"
        # Network string has correct format
        self.assertEqual(str(self.network), expected)

    def test_network_unique_per_user_and_task(self):
        # Cannot create a second network for the same user and task combination
        with self.assertRaises(IntegrityError):
            Network.objects.create(
                name="Duplicate Network",
                subnet="10.0.1.0/24",
                vlan_id=201,
                template=self.network_template,
                user=self.user,
                task=self.task,
            )

    def test_lab_environment_unique_per_user_and_task(self):
        # Cannot create a second lab environment for the same user, task and network combination
        with self.assertRaises(IntegrityError):
            LabEnvironment.objects.create(
                user=self.user,
                task=self.task,
                network=self.network,
            )

    def test_virtual_machine_unique_vmid(self):
        # Check that you cannot have two VMs with the same vmid
        with self.assertRaises(IntegrityError):
            VirtualMachine.objects.create(
                vmid=self.virtual_machine.vmid,
                lab_environment=self.lab_environment,
                template=self.vm_template,
                name="Duplicate VM",
                network=self.network,
            )

    def test_task_vm_template_planned_ip_validation(self):
        invalid_vm_template = TaskVMTemplate(
            configuration=self.task_config,
            template=self.vm_template,
            planned_ip_address="999.999.999.999",
        )
        # Check if invalid ip address fails validation
        with self.assertRaises(ValidationError):
            invalid_vm_template.full_clean()

    def test_user_can_access_task_vm_student_only_if_enrolled(self):
        # Student is not enrolled by default
        self.assertFalse(user_can_access_task_vm(self.user, self.task))

        Enrollment.objects.create(classroom=self.task.project.classroom, student=self.user)
        self.assertTrue(user_can_access_task_vm(self.user, self.task))
