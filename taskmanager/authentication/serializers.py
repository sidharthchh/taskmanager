from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from taskmanager.models import User
from taskmanager.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'userprofile')
        depth = 1


class CreateUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='userprofile.role', allow_blank=False)
    email = serializers.EmailField(allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile')
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        self.update_or_create_profile(user, profile_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'auth_token', 'role',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
