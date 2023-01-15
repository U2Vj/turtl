import secrets
import string

from authentication.models import User
from django.core.mail import send_mail


class Util:
    def send_email(data):
        send_mail(
            data['email_subject'], data['email_body'],'test@mail.com', [data['to_email']]
        )

    # Function to create an account with a randomly generated password and username.
    def create_account(email):
        # Characters to create password and username
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet_password = letters + digits + special_chars
        alphabet_username =  letters + digits

        password = ''
        username = ''
        for i in range(12):
            username += ''.join(secrets.choice(alphabet_username))
            password += ''.join(secrets.choice(alphabet_password))

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            groups='Student'
        )