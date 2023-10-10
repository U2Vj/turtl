from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User
from .serializers import ProfileUpdateSerializer, LoginRefreshSerializer, SendInvitationEmailSerializer,
                          SetNewPasswordSerializer


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


class SendInvitationEmailAPIView(APIView):
    serializer_class = SendInvitationEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(APIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            token = request.data['token']
            uidb64 = request.data['uidb64']
            password = request.data['password']
            password_confirm = request.data['passwordConfirm']
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            if not password == password_confirm:
                raise ValidationError('Your password does not match', 400)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        #serializer.is_valid(raise_exception=True)
