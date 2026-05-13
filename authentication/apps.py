from django.apps import AppConfig

# This file describes the authentication app.
# This app enables authentication via JWT.
# It's based on the tutorial at:
# https://thinkster.io/tutorials/django-json-api/authentication
class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        from django.core.validators import EmailValidator
        if "turtl" not in EmailValidator.domain_allowlist:
            EmailValidator.domain_allowlist = list(EmailValidator.domain_allowlist) + ["turtl"]
