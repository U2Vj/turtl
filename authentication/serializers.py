import logging
from typing import Dict, Any, List

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
import rest_framework_simplejwt.settings
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Invitation


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
        This serializers handles an update request for the current user's profile, i.e. an update of a user object.
        Handles serialization and deserialization of User objects. In TURTL, email addresses are not meant to be
        updated, hence they are not included here.
    """

    id = serializers.IntegerField(read_only=True)

    email = serializers.CharField(read_only=True)

    role = serializers.CharField(read_only=True)
    role_display = serializers.CharField(read_only=True, source='get_role_display')

    # Usernames must be 2 or more and 255 or fewer characters and are optional
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
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'role_display', 'username', 'new_password', 'current_password']

    def validate(self, data):
        # First, we perform the standard validation procedure
        validated_data = super().validate(data)

        # The current password is not necessary for the actual update which is why we can remove it from our
        # pre-validated data
        current_password = validated_data.pop('current_password', None)

        # The actual new password is necessary for the update however, which is why we need to get, not pop it
        new_password = validated_data.get('new_password', None)

        # This section should only apply if the password should be changed and new_password exists
        if new_password is not None:

            if current_password is None:
                raise ValidationError({
                    "current_password": "This field is required when updating a password."
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


class UserSerializer(serializers.ModelSerializer):
    # The ID is the only field that is not read-only because it is used to identify a certain User, e.g. when adding
    # instructors to a classroom (see app 'catalog')
    id = serializers.IntegerField()
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AcceptInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def __init__(self, data=None, **kwargs):
        try:
            self.invitation = Invitation.objects.filter(email=data['email']).first()
            if self.invitation is not None and not self.invitation.token_valid(data['token']):
                self.invitation = None
        except (KeyError, TypeError):
            self.invitation = None
        super().__init__(data=data,**kwargs)


    def validate(self, attrs):
        if not self.invitation:
            raise AuthenticationFailed("No invitation found for the given email address and token.")
        if self.invitation.is_expired:
            raise AuthenticationFailed("Your invitation has already expired.")

        return super().validate(attrs)

    def create(self, validated_data):
        if self.invitation.target_role == self.invitation.TargetRole.INSTRUCTOR:
            user = User.objects.create_instructor(email=validated_data['email'],
                                                  password=validated_data['password'])
        else:
            user = User.objects.create_student(email=validated_data['email'],
                                               password=validated_data['password'])
        user.save()

        # The invitation has been redeemed and accepted, so we can delete it
        self.invitation.delete()

        return user


class InvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=Invitation.objects.all(), message="This email address has already been invited."),
        UniqueValidator(queryset=User.objects.all(), message="A user with this email address already exists.")
    ])
    issuer = UserSerializer(read_only=True)

    target_role_display = serializers.CharField(read_only=True, source='get_target_role_display')

    class Meta:
        model = Invitation
        fields = ['id', 'email', 'target_role', 'target_role_display', 'issuer', 'expiration_date']
        read_only_fields = ['id', 'issuer', 'expiration_date']

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if(validated_data['target_role'] == Invitation.TargetRole.INSTRUCTOR
                and not self.context['request'].user.is_administrator):
            raise PermissionDenied("Only administrators can invite instructors.")

        return validated_data

    def create(self, validated_data) -> Invitation:
        if validated_data['target_role'] == Invitation.TargetRole.INSTRUCTOR:
            invitation = Invitation.objects.invite_instructor(
                email=validated_data['email'],
                issuer=self.context['request'].user
            )
        else:
            invitation = Invitation.objects.invite_student(
                email=validated_data['email'],
                issuer=self.context['request'].user
            )
        return invitation


class BulkInvitationSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(max_length=254),
        allow_empty=False,
        min_length=1,
        max_length=30
    )

    def validate_emails(self, email_array: List[str]):
        errors: List[str] = []
        for email in email_array:
            if Invitation.objects.filter(email__iexact=email).exists():
                errors.append(f"The email address {email} has already been invited.")
            if User.objects.filter(email__iexact=email).exists():
                errors.append(f"A user with the email address {email} already exists.")
        if errors:
            raise ValidationError(errors)
        return email_array

    def create(self, validated_data) -> List[Invitation]:
        invitations: List[Invitation] = []
        for email in validated_data['emails']:
            invitation = Invitation.objects.invite_student(email=email, issuer=self.context['request'].user)
            invitations.append(invitation)
        return invitations

