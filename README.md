# QualiFlow API (Node.js)

QualiFlow é uma API modular para gestão da qualidade escrita em Node.js puro (sem dependências externas) com foco em três pilares:

- **Documentos corporativos com versionamento**
- **Fluxos de trabalho reutilizáveis e processos operacionais**
- **Gestão de atividades para equipes e projetos**

Além dos módulos principais, a API suporta o cadastro de filiais, setores e usuários, permitindo construir soluções completas de governança da qualidade sem precisar de um framework pesado.

## Como executar

1. Certifique-se de ter o Node.js 18 ou superior instalado.
2. Clone este repositório e acesse a pasta do projeto.
3. Execute o servidor de desenvolvimento:

   ```bash
   npm run start
   ```

   O script usa apenas a runtime do Node, portanto nenhuma dependência adicional é necessária.

4. A API ficará disponível em `http://localhost:3000` por padrão. Utilize ferramentas como Insomnia, Postman ou `curl` para enviar requisições HTTP.

> Para alterar a porta, defina a variável de ambiente `PORT` antes de iniciar o servidor (por exemplo, `PORT=4000 npm run start`).

## Estrutura de pastas

```
src/
├── router.js   # Roteador HTTP simples com suporte a parâmetros
├── server.js   # Definição dos endpoints REST e inicialização do servidor
└── store.js    # Armazena dados em memória e implementa as regras de negócio
```

## Principais endpoints

Todos os recursos seguem o padrão `/api/<recurso>`. Abaixo alguns exemplos com seus verbos suportados:

| Recurso | Rotas principais | Descrição |
| --- | --- | --- |
| Filiais | `GET /api/branches`, `POST /api/branches`, `PUT /api/branches/:id`, `DELETE /api/branches/:id` | Cadastro de filiais e controle de dependências |
| Setores | `GET /api/sectors`, `POST /api/sectors`, `PUT /api/sectors/:id` | Vínculo com filiais e documentação |
| Usuários | `GET /api/users`, `POST /api/users`, `PUT /api/users/:id` | Base de usuários para atribuição de tarefas |
| Documentos | `GET /api/documents`, `POST /api/documents` | Cadastro, atualização e associação a filiais/setores |
| Versões de documento | `POST /api/documents/:id/versions` | Incremento de versões com metadados de upload |
| Fluxos de trabalho | `GET /api/workflows`, `POST /api/workflows` | Definição de etapas e descrição |
| Processos | `GET /api/processes`, `POST /api/processes`, `POST /api/processes/:id/advance` | Execução dos fluxos e histórico de etapas |
| Atividades | `GET /api/activities`, `POST /api/processes/:id/activities`, `PATCH /api/activities/:id` | Gestão de tarefas vinculadas a processos |

Todas as respostas retornam JSON no formato `{ "data": ... }` para resultados bem-sucedidos ou `{ "error": { ... } }` para erros.

## Fluxo básico de uso

1. **Cadastre a estrutura organizacional** criando filiais (`/api/branches`) e setores (`/api/sectors`).
2. **Cadastre usuários** responsáveis pelas atividades (`/api/users`).
3. **Registre documentos** e adicione novas versões conforme necessário (`/api/documents`).
4. **Configure fluxos de trabalho** com suas etapas (`/api/workflows`).
5. **Crie processos** baseados nos fluxos definidos (`/api/processes`).
6. **Avance etapas do processo** e registre histórico (`POST /api/processes/:id/advance`).
7. **Controle as atividades** relacionadas aos processos (`/api/processes/:id/activities`).

Como o armazenamento é feito em memória, os dados são reiniciados sempre que o servidor é reiniciado. Integrações reais podem estender `src/store.js` para persistir em bancos de dados relacionais ou NoSQL.

## Próximos passos sugeridos

- Persistir dados em um banco relacional (PostgreSQL/MySQL) ou NoSQL (MongoDB) substituindo a store em memória.
- Adicionar autenticação baseada em tokens JWT para controlar o acesso aos módulos.
- Criar uma interface web (React, Vue ou Angular) utilizando esta API como backend.
- Implementar rotinas de notificação (e-mail/Slack) ao avançar etapas de processos ou alterar status de atividades.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` (caso presente) para mais detalhes.
