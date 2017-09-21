from django.conf import settings
from django.core.mail import send_mail


def send_user_signup_mail(user):
    subject = "Welcome to TaskManager!"
    message = "Welcome to TaskManager!\n\nYou have successfully created an account." \
              "\n\nYour Account Details:\n\nUsername: {} \n\nThanks,\n\nTeam TaskManager."
    message = message.format(user.email)
    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, [user.email],
              fail_silently=False)
