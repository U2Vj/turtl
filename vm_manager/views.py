from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catalog.models import Task
from .models import LabEnvironment
from .proxmox_manager import ProxmoxManager


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_environment(request, task_id):
    """
    Starts a lab environment for the current user and given task
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        # Check if user has a lab environment
        lab_env = LabEnvironment.objects.filter(user=user, task=task).first()

        if not lab_env:
            # Create new environment
            proxmox_manager = ProxmoxManager()
            lab_env = proxmox_manager.create_lab_environment(user, task)
            return Response({
                'status': 'created',
                'message': 'Lab environment created and started successfully',
                'environment_id': lab_env.id
            })
        else:
            # Start existing environment
            proxmox_manager = ProxmoxManager()
            proxmox_manager.start_environment(lab_env)
            lab_env.status = 'active'
            lab_env.save()
            return Response({
                'status': 'started',
                'message': 'Lab environment started successfully',
                'environment_id': lab_env.id
            })

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_environment(request, task_id):
    """
    Stops a lab environment for the current user and given task
    """
    try:
        task = get_object_or_404(Task,  id=task_id)
        user = request.user

        lab_env = LabEnvironment.objects.filter(user=user, task=task).first()

        if not lab_env:
            return Response({
                'status': 'error',
                'message': 'No lab environment found for this task'
            }, status=status.HTTP_404_NOT_FOUND)
        
        lab_env.status = 'cleanup'
        lab_env.save()

        proxmox_manager = ProxmoxManager()
        proxmox_manager.cleanup_environment(user, task, threaded=False)

        return Response({
            'status': 'deleted',
            'message': 'Lab envrionment deleted successfully'
        }, status=status.HTTP_200_OK)
    

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def environment_status(request, task_id):
    """
    Get the status of a lab environment for the current user and task
    """
    try:
        task = get_object_or_404(Task, id=task_id)
        user = request.user

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
        except Exception as e:
            print(f"Warning: Could not sync VM status: {str(e)}")
        
        return Response({
            'status': lab_env.status,
            'environment_id': lab_env.id,
            'created_at': lab_env.created_at,
            'vm_count': lab_env.virtual_machines.count()
        })
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
