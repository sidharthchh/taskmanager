from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_TYPES = (('STUDENT', 'STUDENT'), ('TEACHER', 'TEACHER'), ('ADMIN', 'ADMIN'))
    user = models.OneToOneField(User)
    role = models.CharField(choices=ROLE_TYPES, max_length=31)


class Task(models.Model):
    STATUS_TYPES = (('TODO', 'TODO'), ('DOING', 'DOING'),
                    ('DONE', 'DONE'), ('APPROVED', 'APPROVED'), ('DISAPPROVED', 'DISAPPROVED'))
    title = models.CharField(max_length=1023)
    description = models.TextField()
    status = models.CharField(choices=STATUS_TYPES, max_length=63)
    allotted_to = models.ManyToManyField(User, related_name='allotted_to')
    created_by = models.ForeignKey(User, related_name='created_by')
