from __future__ import unicode_literals, absolute_import

import json

from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from taskmanager.models import Task, TaskAllotment
from taskmanager.permissions import AllowTeacherOrAdmin, IsCreatorOfTask, AllowAdmin, TaskStatusPermission
from taskmanager.serializers import TaskSerializer, AllotTaskSerializer, TaskAllotmentSerializer, TaskCreateSerializer


def health_check(request):
    return HttpResponse("OK", status=200)


def home(request):
    return render(request, 'home.html')


def update_task(request):
    return render(request, 'task_update.html')


def create_task(request):
    return render(request, 'create_task.html')


def delete_task(request):
    return render(request, 'delete_task.html')


def login_page(request):
    return render(request, 'index.html')


class TaskCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
        Creates Tasks only by teacher or admin
    """
    serializer_class = TaskCreateSerializer
    permission_classes = (AllowTeacherOrAdmin,)
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]


class TaskListAllViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
     List Task only for admin
    """
    serializer_class = TaskSerializer
    permission_classes = (AllowAdmin,)
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]


class TaskDeleteViewSet(mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
     Deletes Task only by admin
    """
    serializer_class = TaskSerializer
    permission_classes = (AllowAdmin,)
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]


class TaskListViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
        List Tasks Allotment
    """
    serializer_class = TaskAllotmentSerializer
    permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]
    queryset = TaskAllotment.objects.all()

    def get_queryset(self):
        if self.request.user.userprofile.role == 'STUDENT':
            return TaskAllotment.objects.filter(student=self.request.user)
        elif self.request.user.userprofile.role == "ADMIN":
            return TaskAllotment.objects.all()
        elif self.request.user.userprofile.role == "TEACHER":
            return TaskAllotment.objects.filter(task__created_by=self.request.user)


class TaskStatusUpdateViewSet(mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
    """
        Update the status of the task
    """
    serializer_class = TaskAllotmentSerializer
    permission_classes = (TaskStatusPermission,)
    queryset = TaskAllotment.objects.all()
    authentication_classes = [TokenAuthentication]


class AllotTaskView(GenericAPIView):
    """
        API to allot task to students
    """
    permission_classes = (AllowTeacherOrAdmin, IsCreatorOfTask)
    serializer_class = AllotTaskSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request, task_id):
        students = request.data
        print students
        task_allot_list = []
        for student in students:
            task_allot_list.append(
                TaskAllotment(status="TODO", student_id=student, task_id=task_id)
            )
        print task_allot_list
        TaskAllotment.objects.bulk_create(task_allot_list)
        return HttpResponse(status=201)


@csrf_exempt
def authenticate(request):
    data = json.loads(request.body)
    username = data.get('email', '')
    password = data.get('password', '')

    # authentication of the user, to check if it's active or None
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        token = Token.objects.get(user=user)
        response_data = {"auth_token": token.key}
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    else:
        return HttpResponse("Invalid username or password", status=400)
