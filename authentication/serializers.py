import logging
from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import rest_framework_simplejwt.settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
        This serializers handles a update request for the current user's profile, i.e. an update of a user object.
        Handles serialization and deserialization of User objects. In TURTL, email addresses are not meant to be
        updated, hence they are not included here.
    """

    id = serializers.IntegerField(read_only=True)

    email = serializers.CharField(read_only=True)

    role = serializers.CharField(read_only=True, source='get_role_display')

    # Usernames must be 2 or more and 255 or less characters and are optional
    username = serializers.CharField(min_length=2, max_length=128, allow_null=True, required=False, default=None)

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    new_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    new_password_confirm = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'username', 'new_password', 'new_password_confirm', 'current_password']

    def validate(self, data):
        # First, we perform the standard validation procedure
        validated_data = super().validate(data)

        # The current password and the confirmation is not necessary for the actual update,
        # hence we can remove it from our pre-validated data
        current_password = validated_data.pop('current_password', None)
        new_password_confirm = validated_data.pop('new_password_confirm', None)

        # The actual new password is necessary for the update however, which is why we need to get, not pop it
        new_password = validated_data.get('new_password', None)

        # This section should only apply if the password should be changed and new_password exists
        if new_password is not None:

            if new_password_confirm is None or current_password is None:
                raise ValidationError({
                    "new_password_confirm": "This field is required when updating a password.",
                    "current_password": "This field is required when updating a password."
                })
            if new_password != new_password_confirm:
                raise ValidationError({
                    "new_password_confirm": "Passwords do not match."
                })

            # Check whether the provided current password is correct
            user = self.context['request'].user
            if not user.check_password(current_password):
                raise ValidationError({
                    "current_password": "The current password is not correct."
                })

        return validated_data

    def update(self, instance, validated_data):
        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        new_password = validated_data.pop('new_password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if new_password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(new_password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class LoginRefreshSerializer(serializers.Serializer):
    """
        This serializer is responsible for issuing new access and refresh tokens. It is necessary because the standard
        implementation just copies the claims from the old token. However, we want to update them in case a user has
        updated their profile.

        The following code is based on the default implementation (rest_framework_simplejwt.serializers.
        TokenRefreshSerializer).
    """

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])
        access = refresh.access_token

        # Here, we have to add the potentially updated token claims for the user
        # (in our case, just the username)
        try:
            user = User.objects.get(id=refresh['user_id'])
        except User.DoesNotExist:
            raise TokenError("No user found for given token")

        refresh['username'] = access['username'] = user.username

        data = {"access": str(access)}

        if rest_framework_simplejwt.settings.api_settings.ROTATE_REFRESH_TOKENS:
            if rest_framework_simplejwt.settings.api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    logging.getLogger(__name__).warning("Blacklisting of refresh tokens is enabled but the blacklist"
                                                        "app has not been installed. Skipping...")

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data


class LoginSerializer(TokenObtainPairSerializer):
    """
        This serializer is used to add custom claims (username, role and email) to the JWT tokens used to
        authenticate a user. This information is stored directly in the token and is necessary for the frontend.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['role'] = user.role
        token['role_display'] = user.get_role_display()
        token['email'] = user.email

        return token


class SendInvitationEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email', '')
        if not User.objects.filter(email=email).exists():
            Util.create_account(email=email)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = 'localhost:8080'
            relativeLink = '#/reset-password/' + uidb64 + '/' + token + '/'
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hi, \n Reset your password here:  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return super().validate(data)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = password = serializers.CharField(
        min_length=1,
        write_only=True
    )

    uidb64 = serializers.CharField(
        min_length=1,
        write_only=True
    )

    class Meta:
        fields=['password','token', 'uidb64']

    def validate(self, data):
        try:

            password= data.get('password')
            token = data.get('tok')
            uidb64 = data.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

        return super().validate(data)
