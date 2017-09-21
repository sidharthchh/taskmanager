"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from taskmanager.views import TaskCreateViewSet, TaskListViewSet, TaskDeleteViewSet, TaskStatusUpdateViewSet, \
    TaskListAllViewSet
from . import views
from .authentication import urls as authentication_urls
from .authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks_delete', TaskDeleteViewSet)
router.register(r'tasks_create', TaskCreateViewSet)
router.register(r'tasks_list', TaskListViewSet)
router.register(r'tasks_update', TaskStatusUpdateViewSet)
router.register(r'tasks_list_all', TaskListAllViewSet)

schema_view = get_swagger_view(title='taskmanager APIs')

urlpatterns = [
    url(r'^$', views.login_page),
    url(r'home/$', views.home),
    url(r'update_task/$', views.update_task),
    url(r'create_task/$', views.create_task),
    url(r'delete_task/$', views.delete_task),
    url(r'', include('password_reset.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^swagger/$', schema_view),
    url(r'^api/v1/', include(authentication_urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^healthcheck/$', views.health_check),
    url(r'^login/$', views.authenticate),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'api/v1/allot_task/(?P<task_id>[^/]+)/$', views.AllotTaskView.as_view()),
]
