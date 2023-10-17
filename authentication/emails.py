from django.core.mail import send_mail
from django.conf import settings

def generate_invitation_link(token: str) -> str:
    return f'{settings.FRONTEND_URL}/accept-invitation?token={token}'

def send_invitation_email(invitation, token: str, renew=False) -> None:
    subject = "You have been invited to join TURTL"
    message = (f'Hi there,\n\n'
               f'you have been invited to join TURTL - the VirTUal NetwoRk SecuriTy Lab. To create an account, '
               f'please click here:\n{generate_invitation_link(token)}\n\nThis link is only valid for '
               f'{settings.INVITATION_EXPIRY_DAYS} days.')

    if renew:
        message += ('\n\nYou have already received an invitation previously. '
                    'This is a renewal of your invitation. Your previous invitation links have become invalid.')

    send_mail(subject, message, None, [invitation.email])