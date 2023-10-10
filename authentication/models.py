from datetime import datetime, timedelta

import rules
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _


# This file defines the models used during authentication.
# A model can be stored inside the database.
# Changes to this file require a new migration.
# Check out https://docs.djangoproject.com/en/3.1/topics/db/models/

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password):
        """Create and return a `User` with an email and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_student(self, email, password):
        """
            create and return a student
        """
        user = self.create_user(email, password)
        user.role = user.Role.STUDENT
        user.save()

        return user

    def create_instructor(self, email, password):
        """
            create and return an instructor
        """
        user = self.create_user(email, password)
        user.role = user.Role.INSTRUCTOR
        user.save()

        return user

    def create_administrator(self, email, password):
        """
            create and return an administrator
        """
        user = self.create_user(email, password)
        user.role = user.Role.ADMINISTRATOR
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        return self.create_administrator(email, password)


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(max_length=128, null=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyway, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us, and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # Users can have three different roles within TURTL: administrator, instructor and student.
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR', _('Administrator')
        INSTRUCTOR = 'INSTRUCTOR', _('Instructor')
        STUDENT = 'STUDENT', _('Student')

    role = models.CharField(
        max_length=13,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    # we can use these properties to check which role this user has
    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    @property
    def is_administrator(self):
        return self.role == self.Role.ADMINISTRATOR

    # Only administrators are superusers and only superusers can access the built-in django admin panel (i.e. are
    # members of staff)
    @property
    def is_superuser(self):
        return self.is_administrator

    @property
    def is_staff(self):
        return self.is_superuser

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username
