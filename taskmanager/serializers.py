from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.serializers import UserSerializer
from models import Task, TaskAllotment


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_by',)


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_by',)


class TaskAllotmentSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    task = TaskSerializer()

    class Meta:
        model = TaskAllotment
        fields = ('id', 'status', 'student', 'task',)
        depth = 2

    extra_kwargs = {
        'id': {'read_only': True},
        'student': {'read_only': True},
        'task': {'read_only': True}
    }

    def update(self, instance, validated_data):
        if instance.status == "DONE" and validated_data.get('status', '') in ('DOING', 'APPROVED', 'DISAPPROVED'):
            return super(TaskAllotmentSerializer, self).update(instance, validated_data)
        elif instance.status == "TODO" and validated_data.get('status', '') in ('DOING'):
            return super(TaskAllotmentSerializer, self).update(instance, validated_data)
        elif instance.status == "DOING" and validated_data.get('status', '') in ('TODO', 'DONE'):
            return super(TaskAllotmentSerializer, self).update(instance, validated_data)
        else:
            raise ValidationError("Invalid Transition of status.")


class AllotTaskSerializer(serializers.Serializer):
    user_ids = serializers.ListField()
