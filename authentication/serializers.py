from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
        This serializers handles a update request for the current user's profile, i.e. an update of a user object.
        Handles serialization and deserialization of User objects. In TURTL, email addresses are not meant to be
        updated, hence they are not included here.
    """

    # Usernames must be less than 255 characters and are optional
    username = serializers.CharField(max_length=255, allow_null=True, required=False, default=None)

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
        fields = ['username', 'new_password', 'new_password_confirm', 'current_password']

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


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """
        This serializer is used to add custom claims (username, role and email) to the JWT tokens used to
        authenticate a user. This information is stored directly in the token and is necessary for the frontend.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['role'] = user.role
        token['email'] = user.email

        return token
