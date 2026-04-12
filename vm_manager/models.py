from django.utils import timezone
from django.db import models
from django.conf import settings
from catalog.models import Task
from django.core.validators import validate_ipv4_address


class BridgePoolEntry(models.Model):
    """
    Represents a pre-configured Linux bridge in Proxmox available for assignment to lab envs
    """
    bridge_name = models.CharField(max_length=20, unique=True)  # example: "vmbr100" 
    allocated_to = models.OneToOneField(
        'Network',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bridge_pool_entry'
    )

    class Meta:
        ordering = ['bridge_name']

    def __str__(self):
        status = f"allocated to {self.allocated_to}" if self.allocated_to else "available"
        return f"{self.bridge_name} – {status}"


# Network Instance
class Network(models.Model):
    """
    Represents a network instance for a specific user and task
    """
    name = models.CharField(max_length=255)
    subnet = models.CharField(max_length=20)
    vlan_id = models.IntegerField(unique=True, null=True, blank=True)
    template = models.ForeignKey('NetworkTemplate', on_delete=models.SET_NULL, null=True, related_name="networks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='networks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='networks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'task')
        ]

    def __str__(self):
        return f"{self.name} ({self.subnet}) for {self.user} in {self.task}"


class VMTemplate(models.Model):
    """
    For VM templates in proxmox that can be cloned for tasks
    """
    name = models.CharField(max_length=255)
    template_id = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    #Resources
    cpu_cores = models.IntegerField(default=1)
    memory_mb = models.IntegerField(default=512)
    #Purpose
    PURPOSE_CHOICES = [
        ('USER_SHELL', 'User Shell'),
        ('TASK_SUPPORT', 'Available inside a task as support')
    ]
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)

    def __str__(self):
        return f"{self.name} (ID: {self.template_id})"

class NetworkTemplate(models.Model):
    """
    Network configuration template for interconnected VMs
    """
    name = models.CharField(max_length=255)
    subnet = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.subnet})"


class TaskVMConfiguration(models.Model):
    """
    Links task to VM templates and network config
    Used as a Blueprint for later user environments
    """
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='vm_configuration'
    )
    network_template = models.ForeignKey(
        NetworkTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="task_configurations"
    )

    def __str__(self):
        return f"VM Configuration for {self.task.title}"

class TaskVMTemplate(models.Model):
    """
    Contains VM template needed for a task with configuration
    """

    configuration = models.ForeignKey(
        TaskVMConfiguration,
        on_delete=models.CASCADE,
        related_name='vm_templates'
    )
    template = models.ForeignKey(
        VMTemplate,
        on_delete=models.PROTECT
    )

    planned_ip_address = models.CharField(max_length=15, validators=[validate_ipv4_address], null=True, blank=True)
    cloud_init = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.template.name} for {self.configuration.task.title}"

# User instance of task    
class LabEnvironment(models.Model):
    """
    Groups all parts of the provisioned environment for an individual user and task
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lab_environments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="lab_environments")
    network = models.OneToOneField(Network, on_delete=models.CASCADE, related_name="lab_environments")
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(default=timezone.now, db_index=True)
    stopped_at = models.DateTimeField(null=True, blank=True, db_index=True)

    STATUS_CHOICES = [
        ('provisioning', 'Provisioning'),
        ('starting', 'Starting'),
        ('active', 'Active'),
        ('degraded', 'Degraded'),
        ('stopping', 'Stopping'),
        ('stopped', 'Stopped'),
        ('cleanup', 'Cleanup'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='provisioning')

    class Meta:
        unique_together = ("user", "task")
    
    def __str__(self):
        return f"LabEnvironment for {self.user} in {self.task}"

# Instance of a VM inside a task
class VirtualMachine(models.Model):
    """
    Represents an VM instance for a specific user and task
    """
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('paused', 'Paused'),
        ('suspended', 'Suspended'),
        ('creating', 'Creating'),
        ('error', 'Error'),
    ]
    #The ID of the VM in Proxmox
    vmid = models.IntegerField(unique=True)
    # Environment the VM belongs to
    lab_environment = models.ForeignKey(
        LabEnvironment,
        on_delete=models.CASCADE,
        related_name="virtual_machines"
    )
    #template used to create the VM
    template = models.ForeignKey(VMTemplate, on_delete=models.SET_NULL, null=True)
    #VM Name in Proxmox
    name = models.CharField(max_length=255)
    #Current status of the VM
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='creating')
    status_changed_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)
    #Network config
    network = models.ForeignKey('Network', on_delete=models.SET_NULL, null=True, related_name='vms')
    assigned_ip_address = models.GenericIPAddressField(null=True, blank=True)
    #Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
