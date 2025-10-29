# QualiFlow

QualiFlow é um sistema web modular para gestão da qualidade com foco em documentação, fluxos de trabalho, processos e atividades. O projeto é construído com Django e Django REST Framework, oferecendo uma API pronta para integração com aplicativos web e móveis.

## Funcionalidades principais

- **Gestão de documentos**: cadastro de documentos corporativos, controle de versões com upload de arquivos e histórico completo.
- **Fluxos de trabalho**: criação de fluxos reutilizáveis com etapas configuráveis, responsáveis e prazos estimados.
- **Processos operacionais**: geração de processos que respeitam as etapas do fluxo associado, acompanhando status e responsáveis.
- **Gestão de atividades**: organização de tarefas de equipes e projetos com prioridade, status e datas de conclusão.
- **Estrutura organizacional**: cadastro de filiais e setores, vinculados a documentos, processos e atividades.
- **Gestão de usuários**: integração com o modelo de usuários do Django, permitindo controle de acesso e visibilidade por filial/setor.

## Estrutura do projeto

```
qualiflow/
├── manage.py
├── qualiflow/        # Configurações do projeto Django
└── quality/          # Aplicação principal de gestão da qualidade
```

A aplicação `quality` concentra os modelos, serializers e viewsets responsáveis por cada módulo do sistema, expondo endpoints RESTful prontos para uso.

## Configuração do ambiente

1. Crie e ative um ambiente virtual Python 3.11 (ou superior).
2. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute as migrações e crie um superusuário para acessar o painel administrativo:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Suba o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

A API estará disponível em `http://localhost:8000/api/` e o painel administrativo em `http://localhost:8000/admin/`.

## Endpoints principais

| Recurso | Endpoint | Descrição |
| ------- | -------- | --------- |
| Filiais | `/api/branches/` | CRUD completo para filiais |
| Setores | `/api/sectors/` | Cadastro e vínculo com filiais |
| Documentos | `/api/documents/` | Gestão de documentos e upload de novas versões |
| Versões de documentos | `/api/document-versions/` | Histórico completo de versões |
| Fluxos de trabalho | `/api/workflows/` | Definição de fluxos reutilizáveis |
| Etapas de fluxo | `/api/workflow-steps/` | Configuração de etapas e responsáveis |
| Processos | `/api/processes/` | Execução de processos baseados em fluxos |
| Etapas de processo | `/api/process-steps/` | Acompanhamento do status das etapas |
| Atividades | `/api/activities/` | Gestão de tarefas por equipe ou projeto |
| Usuários | `/api/users/` | Consulta de usuários (somente administradores) |

Os endpoints suportam autenticação básica e de sessão através da configuração padrão do Django REST Framework.

## Próximos passos sugeridos

- Configurar autenticação JWT ou OAuth2 para cenários de produção.
- Criar interface frontend dedicada (React, Vue ou Angular) integrada à API.
- Adicionar regras de negócio específicas, como notificações automáticas e relatórios.
