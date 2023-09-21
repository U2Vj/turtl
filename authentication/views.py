from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User
from .serializers import ProfileUpdateSerializer, LoginRefreshSerializer


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


class TestProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'token_valid': True})
