from django.contrib import admin
from .models import Network, VMTemplate, NetworkTemplate, TaskVMConfiguration, TaskVMTemplate, LabEnvironment, VirtualMachine
# Register your models here.

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ['name', 'subnet', 'vlan_id', 'user', 'task', 'created_at']
    list_filter = ['user', 'task', 'created_at']

@admin.register(VMTemplate)
class VMTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_id', 'purpose', 'cpu_cores', 'memory_mb']
    list_filter = ['purpose']

@admin.register(NetworkTemplate)
class NetworkTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subnet', 'vlan_id']
    list_filter = ['vlan_id']

@admin.register(TaskVMConfiguration)
class TaskVMConfigurationAdmin(admin.ModelAdmin):
    list_display = ['task', 'network_template', 'allow_internet_access', 'max_runtime_hours', 'auto_cleanup_after_hours']
    list_filter = ['allow_internet_access', 'max_runtime_hours']

@admin.register(TaskVMTemplate)
class TaskVMTemplateAdmin(admin.ModelAdmin):
    list_display = ['template', 'configuration', 'planned_ip_address']
    list_filter = ['template', 'configuration']

@admin.register(LabEnvironment)
class LabEnvironmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'status', 'network', 'created_at']
    list_filter = ['status', 'user', 'task', 'created_at']

@admin.register(VirtualMachine)
class VirtualMachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'vmid', 'status', 'lab_environment', 'template', 'assigned_ip_address', 'created_at']
    list_filter = ['status', 'template', 'lab_environment', 'created_at']
    