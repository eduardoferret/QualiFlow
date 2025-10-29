from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sector
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by_display = serializers.StringRelatedField(source='uploaded_by', read_only=True)

    class Meta:
        model = models.DocumentVersion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DocumentSerializer(serializers.ModelSerializer):
    created_by_display = serializers.StringRelatedField(source='created_by', read_only=True)
    versions = DocumentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Document
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'current_version',
        )


class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowStep
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class WorkflowSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)
    created_by_display = serializers.StringRelatedField(source='created_by', read_only=True)

    class Meta:
        model = models.Workflow
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProcessStepSerializer(serializers.ModelSerializer):
    workflow_step_display = serializers.StringRelatedField(source='workflow_step', read_only=True)
    assigned_to_display = serializers.StringRelatedField(source='assigned_to', read_only=True)

    class Meta:
        model = models.ProcessStep
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProcessSerializer(serializers.ModelSerializer):
    steps = ProcessStepSerializer(many=True, read_only=True)
    created_by_display = serializers.StringRelatedField(source='created_by', read_only=True)

    class Meta:
        model = models.Process
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ActivitySerializer(serializers.ModelSerializer):
    created_by_display = serializers.StringRelatedField(source='created_by', read_only=True)
    assigned_to_display = serializers.StringRelatedField(source='assigned_to', read_only=True)

    class Meta:
        model = models.Activity
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    branch_memberships = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            get_user_model().USERNAME_FIELD,
            'first_name',
            'last_name',
            'email',
            'is_active',
            'branch_memberships',
        )
        read_only_fields = ('id',)

    def get_branch_memberships(self, obj):
        branches = models.Branch.objects.filter(processes__created_by=obj).distinct()
        return BranchSerializer(branches, many=True).data
