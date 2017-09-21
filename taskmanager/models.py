from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from taskmanager.authentication.mail_helper import send_user_signup_mail


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class UserProfile(models.Model):
    ROLE_TYPES = (('STUDENT', 'STUDENT'), ('TEACHER', 'TEACHER'), ('ADMIN', 'ADMIN'))
    user = models.OneToOneField(User)
    role = models.CharField(choices=ROLE_TYPES, max_length=31)


class Task(models.Model):
    title = models.CharField(max_length=1023)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='created_by')


class TaskAllotment(models.Model):
    STATUS_TYPES = (('TODO', 'TODO'), ('DOING', 'DOING'),
                    ('DONE', 'DONE'), ('APPROVED', 'APPROVED'), ('DISAPPROVED', 'DISAPPROVED'))
    status = models.CharField(choices=STATUS_TYPES, max_length=63, default="TODO")
    student = models.ForeignKey(User)
    task = models.ForeignKey(Task)


def user_created(sender, instance, created, **kwargs):
    if created:
        send_user_signup_mail(instance)


signals.post_save.connect(user_created, sender=User)
