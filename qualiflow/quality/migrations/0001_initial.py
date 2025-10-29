from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Filial',
                'verbose_name_plural': 'Filiais',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('branch', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='sectors', to='quality.branch')),
            ],
            options={
                'verbose_name': 'Setor',
                'verbose_name_plural': 'Setores',
                'ordering': ['branch__name', 'name'],
                'unique_together': {('branch', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('current_version', models.PositiveIntegerField(default=1)),
                ('branch', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='documents', to='quality.branch')),
                ('created_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='documents', to=settings.AUTH_USER_MODEL)),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='documents', to='quality.sector')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('branch', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='workflows', to='quality.branch')),
                ('created_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='workflows', to=settings.AUTH_USER_MODEL)),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='workflows', to='quality.sector')),
            ],
            options={
                'verbose_name': 'Fluxo de Trabalho',
                'verbose_name_plural': 'Fluxos de Trabalho',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('planned', 'Planejado'), ('in_progress', 'Em andamento'), ('completed', 'Concluído'), ('cancelled', 'Cancelado')], default='planned', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='processes', to='quality.branch')),
                ('created_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='processes', to=settings.AUTH_USER_MODEL)),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='processes', to='quality.sector')),
                ('workflow', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='processes', to='quality.workflow')),
            ],
            options={
                'verbose_name': 'Processo',
                'verbose_name_plural': 'Processos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('todo', 'A Fazer'), ('in_progress', 'Em andamento'), ('review', 'Em revisão'), ('done', 'Concluída'), ('blocked', 'Bloqueada')], default='todo', max_length=20)),
                ('priority', models.CharField(choices=[('low', 'Baixa'), ('medium', 'Média'), ('high', 'Alta'), ('critical', 'Crítica')], default='medium', max_length=20)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='activities', to=settings.AUTH_USER_MODEL)),
                ('branch', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='activities', to='quality.branch')),
                ('created_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='created_activities', to=settings.AUTH_USER_MODEL)),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='activities', to='quality.process')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='activities', to='quality.sector')),
            ],
            options={
                'verbose_name': 'Atividade',
                'verbose_name_plural': 'Atividades',
                'ordering': ['-priority', 'due_date'],
            },
        ),
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to='documents/')),
                ('notes', models.TextField(blank=True)),
                ('document', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='versions', to='quality.document')),
                ('uploaded_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='document_versions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Versão do Documento',
                'verbose_name_plural': 'Versões de Documentos',
                'ordering': ['-version'],
                'unique_together': {('document', 'version')},
            },
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('estimated_days', models.PositiveIntegerField(default=0)),
                ('responsible_sector', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='workflow_steps', to='quality.sector')),
                ('workflow', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='steps', to='quality.workflow')),
            ],
            options={
                'verbose_name': 'Etapa do Fluxo',
                'verbose_name_plural': 'Etapas do Fluxo',
                'ordering': ['workflow', 'order'],
                'unique_together': {('workflow', 'order')},
            },
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('in_progress', 'Em andamento'), ('done', 'Concluído'), ('blocked', 'Bloqueado')], default='pending', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='assigned_process_steps', to=settings.AUTH_USER_MODEL)),
                ('process', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='steps', to='quality.process')),
                ('workflow_step', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='process_steps', to='quality.workflowstep')),
            ],
            options={
                'verbose_name': 'Etapa do Processo',
                'verbose_name_plural': 'Etapas do Processo',
                'ordering': ['process', 'workflow_step__order'],
                'unique_together': {('process', 'workflow_step')},
            },
        ),
    ]
