from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

from taskmanager.models import UserProfile, Task


class AllowTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.userprofile.role in ('ADMIN', 'TEACHER'):
                return True
        except UserProfile.DoesNotExist:
            return False


class IsCreatorOfTask(permissions.BasePermission):
    def has_permission(self, request, view):
        task_id = request.parser_context.get('kwargs', {}).get('task_id', 0)
        try:
            if request.user.userprofile.role == 'ADMIN':
                return True
            elif request.user.userprofile.role == 'TEACHER' \
                and Task.objects.filter(id=task_id, created_by=request.user).exists():
                return True
        except UserProfile.DoesNotExist:
            return False
        return False


class AllowAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.userprofile.role in ('ADMIN'):
                return True
        except UserProfile.DoesNotExist:
            return False


class TaskStatusPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        status = request.data.get('status')
        try:
            if request.user.userprofile.role == 'STUDENT' and status in ('TODO', 'DOING', 'DONE'):
                return True
            elif request.user.userprofile.role in ('ADMIN', 'TEACHER') \
                and status in ('APPROVED', 'DISAPPROVED'):
                return True
            else:
                return False
        except UserProfile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.userprofile.role == 'STUDENT' \
                and obj.student == request.user:
                return True
            elif request.user.userprofile.role == 'TEACHER' \
                and obj.task.created_by == request.user:
                return True
            elif request.user.userprofile.role == "ADMIN":
                return True
            else:
                return False
        except UserProfile.DoesNotExist:
            return False
