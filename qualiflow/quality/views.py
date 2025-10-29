from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectorViewSet(viewsets.ModelViewSet):
    queryset = models.Sector.objects.select_related('branch')
    serializer_class = serializers.SectorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.select_related('branch', 'sector', 'created_by').prefetch_related(
        'versions'
    )
    serializer_class = serializers.DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload')
    def upload_version(self, request, pk=None):
        document = self.get_object()
        serializer = serializers.DocumentVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        next_version = document.current_version + 1
        serializer.save(
            document=document,
            uploaded_by=request.user,
            version=next_version,
        )
        document.current_version = next_version
        document.save(update_fields=['current_version', 'updated_at'])
        document_serializer = self.get_serializer(document)
        return Response(document_serializer.data, status=status.HTTP_201_CREATED)


class DocumentVersionViewSet(viewsets.ModelViewSet):
    queryset = models.DocumentVersion.objects.select_related('document', 'uploaded_by')
    serializer_class = serializers.DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = models.Workflow.objects.select_related('branch', 'sector', 'created_by').prefetch_related(
        'steps'
    )
    serializer_class = serializers.WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='steps')
    def create_step(self, request, pk=None):
        workflow = self.get_object()
        serializer = serializers.WorkflowStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workflow=workflow)
        workflow_serializer = self.get_serializer(workflow)
        return Response(workflow_serializer.data, status=status.HTTP_201_CREATED)


class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = models.WorkflowStep.objects.select_related('workflow', 'responsible_sector')
    serializer_class = serializers.WorkflowStepSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = models.Process.objects.select_related(
        'workflow', 'branch', 'sector', 'created_by'
    ).prefetch_related('steps')
    serializer_class = serializers.ProcessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        process = serializer.save(created_by=self.request.user)
        steps_to_create = []
        for step in process.workflow.steps.all():
            steps_to_create.append(
                models.ProcessStep(
                    process=process,
                    workflow_step=step,
                    status=models.ProcessStep.StepStatus.PENDING,
                )
            )
        models.ProcessStep.objects.bulk_create(steps_to_create)


class ProcessStepViewSet(viewsets.ModelViewSet):
    queryset = models.ProcessStep.objects.select_related(
        'process', 'workflow_step', 'assigned_to'
    )
    serializer_class = serializers.ProcessStepSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = models.Activity.objects.select_related(
        'process', 'branch', 'sector', 'created_by', 'assigned_to'
    )
    serializer_class = serializers.ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]
