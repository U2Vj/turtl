from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from turtl.utils.permissions import AutoPermissionViewSetWithListMixin

from .models import User, Invitation
from .serializers import (ProfileUpdateSerializer, LoginRefreshSerializer,
                          InvitationSerializer, AcceptInvitationSerializer, BulkInvitationSerializer, UserSerializer)


class ProfileUpdateView(RetrieveUpdateAPIView):
    """
        This defines an API view to update a user's profile. It only accepts PUT-Requests
    """
    # A user must be authenticated to update a user
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # serialize, validate, save pattern
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginRefreshView(TokenRefreshView):
    """
        This view is responsible for receiving a refresh token and issuing a new pair of access and refresh tokens.
        It is necessary because the standard implementation simply copies the token claims from the old token when
        refreshing. This poses a problem when updating a user's profile since the username (which is part of a token's
        payload) might have been changed.
    """
    serializer_class = LoginRefreshSerializer


class InvitationViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class BulkInvitationViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = BulkInvitationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class MyInvitationsViewSet(InvitationViewSet):
    def get_queryset(self):
        return Invitation.objects.filter(issuer=self.request.user).all()


class AcceptInvitationView(CreateAPIView):
    serializer_class = AcceptInvitationSerializer


class RenewInvitationView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk: int = None):
        invitation = Invitation.objects.filter(id=pk).first()

        if not request.user.has_perm('authentication.change_invitation', invitation):
            raise PermissionDenied
        if not invitation:
            raise NotFound

        invitation.renew()

        return Response(status=status.HTTP_200_OK)


class InstructorViewSet(ModelViewSet):
    """
        This view returns a list of all Instructors or Administrators (everyone who can manage a Classroom). It is
        available to all signed-in Users of TURTL.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(Q(role=User.Role.INSTRUCTOR) | Q(role=User.Role.ADMINISTRATOR))
    serializer_class = UserSerializer
