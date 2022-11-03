from django.apps import AppConfig

# This file describes the authentication app.
# This app enables authentication via JWT.
# It's based on the tutorial at:
# https://thinkster.io/tutorials/django-json-api/authentication
class AuthenticationConfig(AppConfig):
    name = 'authentication'
