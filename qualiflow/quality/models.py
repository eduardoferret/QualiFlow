from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Branch(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Filial')
        verbose_name_plural = _('Filiais')
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Sector(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sectors')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Setor')
        verbose_name_plural = _('Setores')
        unique_together = ('branch', 'name')
        ordering = ['branch__name', 'name']

    def __str__(self) -> str:
        return f"{self.branch.code} - {self.name}"


class Document(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='documents'
    )
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='documents')
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name='documents', null=True, blank=True
    )
    current_version = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Documento')
        verbose_name_plural = _('Documentos')
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return self.title


class DocumentVersion(TimeStampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField()
    file = models.FileField(upload_to='documents/')
    notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='document_versions'
    )

    class Meta:
        verbose_name = _('Versão do Documento')
        verbose_name_plural = _('Versões de Documentos')
        unique_together = ('document', 'version')
        ordering = ['-version']

    def __str__(self) -> str:
        return f"{self.document.title} v{self.version}"


class Workflow(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='workflows'
    )
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='workflows')
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name='workflows', null=True, blank=True
    )

    class Meta:
        verbose_name = _('Fluxo de Trabalho')
        verbose_name_plural = _('Fluxos de Trabalho')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class WorkflowStep(TimeStampedModel):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    responsible_sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name='workflow_steps', null=True, blank=True
    )
    estimated_days = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Etapa do Fluxo')
        verbose_name_plural = _('Etapas do Fluxo')
        ordering = ['workflow', 'order']
        unique_together = ('workflow', 'order')

    def __str__(self) -> str:
        return f"{self.workflow.name} - {self.name}"


class Process(TimeStampedModel):
    class ProcessStatus(models.TextChoices):
        PLANNED = 'planned', _('Planejado')
        IN_PROGRESS = 'in_progress', _('Em andamento')
        COMPLETED = 'completed', _('Concluído')
        CANCELLED = 'cancelled', _('Cancelado')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT, related_name='processes')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='processes')
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name='processes', null=True, blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='processes'
    )
    status = models.CharField(
        max_length=20, choices=ProcessStatus.choices, default=ProcessStatus.PLANNED
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Processo')
        verbose_name_plural = _('Processos')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name


class ProcessStep(TimeStampedModel):
    class StepStatus(models.TextChoices):
        PENDING = 'pending', _('Pendente')
        IN_PROGRESS = 'in_progress', _('Em andamento')
        DONE = 'done', _('Concluído')
        BLOCKED = 'blocked', _('Bloqueado')

    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='steps')
    workflow_step = models.ForeignKey(
        WorkflowStep, on_delete=models.PROTECT, related_name='process_steps'
    )
    status = models.CharField(
        max_length=20, choices=StepStatus.choices, default=StepStatus.PENDING
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_process_steps',
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Etapa do Processo')
        verbose_name_plural = _('Etapas do Processo')
        unique_together = ('process', 'workflow_step')
        ordering = ['process', 'workflow_step__order']

    def __str__(self) -> str:
        return f"{self.process.name} - {self.workflow_step.name}"


class Activity(TimeStampedModel):
    class ActivityStatus(models.TextChoices):
        TODO = 'todo', _('A Fazer')
        IN_PROGRESS = 'in_progress', _('Em andamento')
        REVIEW = 'review', _('Em revisão')
        DONE = 'done', _('Concluída')
        BLOCKED = 'blocked', _('Bloqueada')

    class ActivityPriority(models.TextChoices):
        LOW = 'low', _('Baixa')
        MEDIUM = 'medium', _('Média')
        HIGH = 'high', _('Alta')
        CRITICAL = 'critical', _('Crítica')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    process = models.ForeignKey(
        Process, on_delete=models.SET_NULL, related_name='activities', null=True, blank=True
    )
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='activities')
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name='activities', null=True, blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_activities'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='activities', null=True, blank=True
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ActivityStatus.choices, default=ActivityStatus.TODO
    )
    priority = models.CharField(
        max_length=20, choices=ActivityPriority.choices, default=ActivityPriority.MEDIUM
    )

    class Meta:
        verbose_name = _('Atividade')
        verbose_name_plural = _('Atividades')
        ordering = ['-priority', 'due_date']

    def __str__(self) -> str:
        return self.title
