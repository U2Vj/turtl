import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catalog.models import Task
from .proxmox_manager import ProxmoxManager
from .access import user_can_access_task_vm
from .models import VirtualMachine, LabEnvironment, TaskVMConfiguration
from django.utils import timezone

logger = logging.getLogger(__name__)


def _forbidden_task_vm_access():
    return Response(
        {
            'status': 'error',
            'detail': 'You do not have access to VM resources for this task'
        },
        status=status.HTTP_403_FORBIDDEN
    )


def _internal_vm_error(detail: str, error_code: str):
    return Response(
        {
            'status': 'error',
            'detail': detail,
            'error_code': error_code,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_environment(request, task_id):
    """
    Starts a lab environment for the current user and given task
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        if not user_can_access_task_vm(user, task):
            return _forbidden_task_vm_access()

        # Check if user has a lab environment
        lab_env = LabEnvironment.objects.filter(user=user, task=task).first()

        proxmox_manager = ProxmoxManager()
        if not lab_env:
            # Create new environment
            lab_env = proxmox_manager.create_lab_environment(user, task)
            return Response({
                'status': 'created',
                'message': 'Lab environment created and started successfully',
                'environment_id': lab_env.id
            })
        else:
            # Start existing environment
            started = proxmox_manager.start_environment(lab_env)
            if (started):
                return Response({
                    'status': 'started',
                    'message': 'Lab environment started successfully',
                    'environment_id': lab_env.id
                })
            else:
                return Response({
                    'status': 'error',
                    'detail': 'VMs for LabEnvironment could not be started. Check Proxmox logs',
                    'environment_id': lab_env.id
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception:
        logger.exception(
            "Failed to start lab environment for task_id=%s user_id=%s",
            task_id,
            getattr(request.user, "id", None),
        )
        return _internal_vm_error(
            detail='An unexpected error occurred while starting the lab environment.',
            error_code='ENVIRONMENT_START_FAILED',
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_environment(request, task_id):
    """
    Stops a lab environment for the current user and given task
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        if not user_can_access_task_vm(user, task):
            return _forbidden_task_vm_access()

        lab_env = LabEnvironment.objects.filter(user=user, task=task).first()

        if not lab_env:
            return Response({
                'status': 'error',
                'detail': 'No lab environment found for this task'
            }, status=status.HTTP_404_NOT_FOUND)
        
        proxmox_manager = ProxmoxManager()
        proxmox_manager.stop_environment(lab_env)

        return Response({
            'status': 'stopped',
            'message': 'Lab environment stopped successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception:
        logger.exception(
            "Failed to stop lab environment for task_id=%s user_id=%s",
            task_id,
            getattr(request.user, "id", None),
        )
        return _internal_vm_error(
            detail='An unexpected error occurred while stopping the lab environment.',
            error_code='ENVIRONMENT_STOP_FAILED',
        )

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cleanup_environment(request, task_id):
    """
    Stops and removes a lab environment for the current user and given task
    """
    try:
        task = get_object_or_404(Task,  id=task_id)
        user = request.user

        if not user_can_access_task_vm(user, task):
            return _forbidden_task_vm_access()
        
        proxmox_manager = ProxmoxManager()
        cleanup_result = proxmox_manager.cleanup_environment(user, task)

        if cleanup_result == 'deleted':
            return Response({
                'status': 'deleted',
                'message': 'Lab environment deleted successfully'
            }, status=status.HTTP_200_OK)

        if cleanup_result == 'not_found':
            return Response({
                'status': 'error',
                'detail': 'No lab environment found for this task'
            }, status=status.HTTP_404_NOT_FOUND)

        if cleanup_result == 'locked':
            return Response({
                'status': 'error',
                'detail': 'Cleanup is already in progress. Please retry shortly.'
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            'status': 'error',
            'detail': 'Cleanup could not be completed right now. Please retry.',
            'error_code': 'ENVIRONMENT_CLEANUP_RETRY',
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    

    except Exception:
        logger.exception(
            "Failed to clean up lab environment for task_id=%s user_id=%s",
            task_id,
            getattr(request.user, "id", None),
        )
        return _internal_vm_error(
            detail='An unexpected error occurred while cleaning up the lab environment.',
            error_code='ENVIRONMENT_CLEANUP_FAILED',
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def environment_status(request, task_id):
    """
    Get the status of a lab environment for the current user and task
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        if not user_can_access_task_vm(user, task):
            return _forbidden_task_vm_access()

        lab_env = LabEnvironment.objects.filter(user=user, task=task).first()

        if not lab_env:
            return Response({
                'status': 'not_created',
                'message': 'No lab environment exists for this task'
            })
        
        # Synchronize VM status
        try:
            proxmox_manager = ProxmoxManager()
            proxmox_manager.sync_vm_status(lab_env)
        except Exception:
            logger.warning(
                "Could not sync VM status for environment_id=%s task_id=%s user_id=%s",
                lab_env.id,
                task_id,
                getattr(request.user, "id", None),
                exc_info=True,
            )
        
        if lab_env.status == 'active':
            lab_env.last_seen_at = timezone.now()
            lab_env.save(update_fields=['last_seen_at'])
        
        return Response({
            'status': lab_env.status,
            'environment_id': lab_env.id,
            'created_at': lab_env.created_at,
            'vm_count': lab_env.virtual_machines.count()
        })
    
    except Exception:
        logger.exception(
            "Failed to retrieve environment status for task_id=%s user_id=%s",
            task_id,
            getattr(request.user, "id", None),
        )
        return _internal_vm_error(
            detail='An unexpected error occurred while fetching environment status.',
            error_code='ENVIRONMENT_STATUS_FAILED',
        )
            
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vnc_ticket(request, task_id):
    """
    Returns a VNC ticket for the user's USER_SHELL VM of the given task.
    The frontend uses this as VNC password via noVNC credentials.
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        if not user_can_access_task_vm(user, task):
            return _forbidden_task_vm_access()

        vm = VirtualMachine.objects.filter(
            lab_environment__user=user,
            lab_environment__task=task,
            template__purpose='USER_SHELL'
        ).first()

        if not vm:
            return Response({
                'status': 'error',
                'detail': 'No USER_SHELL VM found for this task/user'
            }, status=status.HTTP_404_NOT_FOUND)

        pm = ProxmoxManager()
        node = pm.get_vm_node(vm.vmid)
        ticket_data = pm.get_vm_console_ticket(node, vm.vmid)

        return Response({
            'status': 'ok',
            'ticket': ticket_data['ticket'],
            'port': ticket_data['port'],
            'node': node,
        })
    except Exception:
        logger.exception(
            "Failed to get VNC ticket for task_id=%s user_id=%s",
            task_id,
            getattr(request.user, "id", None),
        )
        return _internal_vm_error(
            detail='An unexpected error occurred while fetching the VNC ticket.',
            error_code='VNC_TICKET_FAILED',
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_task_vm_config(request, task_id: int):
    """
    Checks if there is a TaskVMConfiguration for the specific Task
    """
    task = get_object_or_404(Task, id=task_id)
    if not user_can_access_task_vm(request.user, task):
        return _forbidden_task_vm_access()

    exists = TaskVMConfiguration.objects.filter(task_id=task_id).exists()
    return Response({"has_config": exists})
            
