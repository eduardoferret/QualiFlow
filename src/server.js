const http = require('http');
const Router = require('./router');
const store = require('./store');

const router = new Router();

const ok = (data) => ({ data });

// Branches
router.register('GET', '/api/branches', async ({ json }) => {
  json(200, ok(store.listBranches()));
});

router.register('POST', '/api/branches', async ({ body, json }) => {
  const branch = store.createBranch(body || {});
  json(201, ok(branch));
});

router.register('GET', '/api/branches/:id', async ({ params, json }) => {
  const branch = store.getBranch(params.id);
  if (!branch) {
    const error = new Error('Filial não encontrada.');
    error.status = 404;
    throw error;
  }
  json(200, ok(branch));
});

router.register('PUT', '/api/branches/:id', async ({ params, body, json }) => {
  const branch = store.updateBranch(params.id, body || {});
  json(200, ok(branch));
});

router.register('DELETE', '/api/branches/:id', async ({ params, json }) => {
  const branch = store.deleteBranch(params.id);
  json(200, ok(branch));
});

// Sectors
router.register('GET', '/api/sectors', async ({ json }) => {
  json(200, ok(store.listSectors()));
});

router.register('POST', '/api/sectors', async ({ body, json }) => {
  const sector = store.createSector(body || {});
  json(201, ok(sector));
});

router.register('GET', '/api/sectors/:id', async ({ params, json }) => {
  const sector = store.getSector(params.id);
  if (!sector) {
    const error = new Error('Setor não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(sector));
});

router.register('PUT', '/api/sectors/:id', async ({ params, body, json }) => {
  const sector = store.updateSector(params.id, body || {});
  json(200, ok(sector));
});

router.register('DELETE', '/api/sectors/:id', async ({ params, json }) => {
  const sector = store.deleteSector(params.id);
  json(200, ok(sector));
});

// Users
router.register('GET', '/api/users', async ({ json }) => {
  json(200, ok(store.listUsers()));
});

router.register('POST', '/api/users', async ({ body, json }) => {
  const user = store.createUser(body || {});
  json(201, ok(user));
});

router.register('GET', '/api/users/:id', async ({ params, json }) => {
  const user = store.getUser(params.id);
  if (!user) {
    const error = new Error('Usuário não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(user));
});

router.register('PUT', '/api/users/:id', async ({ params, body, json }) => {
  const user = store.updateUser(params.id, body || {});
  json(200, ok(user));
});

router.register('DELETE', '/api/users/:id', async ({ params, json }) => {
  const user = store.deleteUser(params.id);
  json(200, ok(user));
});

// Documents
router.register('GET', '/api/documents', async ({ json }) => {
  json(200, ok(store.listDocuments()));
});

router.register('POST', '/api/documents', async ({ body, json }) => {
  const document = store.createDocument(body || {});
  json(201, ok(document));
});

router.register('GET', '/api/documents/:id', async ({ params, json }) => {
  const document = store.getDocument(params.id);
  if (!document) {
    const error = new Error('Documento não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(document));
});

router.register('PUT', '/api/documents/:id', async ({ params, body, json }) => {
  const document = store.updateDocument(params.id, body || {});
  json(200, ok(document));
});

router.register('DELETE', '/api/documents/:id', async ({ params, json }) => {
  const document = store.deleteDocument(params.id);
  json(200, ok(document));
});

router.register('POST', '/api/documents/:id/versions', async ({ params, body, json }) => {
  const version = store.addDocumentVersion(params.id, body || {});
  json(201, ok(version));
});

// Workflows
router.register('GET', '/api/workflows', async ({ json }) => {
  json(200, ok(store.listWorkflows()));
});

router.register('POST', '/api/workflows', async ({ body, json }) => {
  const workflow = store.createWorkflow(body || {});
  json(201, ok(workflow));
});

router.register('GET', '/api/workflows/:id', async ({ params, json }) => {
  const workflow = store.getWorkflow(params.id);
  if (!workflow) {
    const error = new Error('Fluxo de trabalho não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(workflow));
});

router.register('PUT', '/api/workflows/:id', async ({ params, body, json }) => {
  const workflow = store.updateWorkflow(params.id, body || {});
  json(200, ok(workflow));
});

router.register('DELETE', '/api/workflows/:id', async ({ params, json }) => {
  const workflow = store.deleteWorkflow(params.id);
  json(200, ok(workflow));
});

// Processes
router.register('GET', '/api/processes', async ({ json }) => {
  json(200, ok(store.listProcesses()));
});

router.register('POST', '/api/processes', async ({ body, json }) => {
  const process = store.createProcess(body || {});
  json(201, ok(process));
});

router.register('GET', '/api/processes/:id', async ({ params, json }) => {
  const process = store.getProcess(params.id);
  if (!process) {
    const error = new Error('Processo não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(process));
});

router.register('PUT', '/api/processes/:id', async ({ params, body, json }) => {
  const process = store.updateProcess(params.id, body || {});
  json(200, ok(process));
});

router.register('DELETE', '/api/processes/:id', async ({ params, json }) => {
  const process = store.deleteProcess(params.id);
  json(200, ok(process));
});

router.register('POST', '/api/processes/:id/advance', async ({ params, body, json }) => {
  const process = store.advanceProcess(params.id, body || {});
  json(200, ok(process));
});

router.register('GET', '/api/processes/:id/history', async ({ params, json }) => {
  const process = store.getProcess(params.id);
  if (!process) {
    const error = new Error('Processo não encontrado.');
    error.status = 404;
    throw error;
  }
  json(200, ok(process.history));
});

// Activities
router.register('GET', '/api/activities', async ({ query, json }) => {
  const activities = store.listActivities({
    processId: query.processId || null,
    status: query.status || null
  });
  json(200, ok(activities));
});

router.register('GET', '/api/processes/:id/activities', async ({ params, json }) => {
  const activities = store.listActivities({ processId: params.id });
  json(200, ok(activities));
});

router.register('POST', '/api/processes/:id/activities', async ({ params, body, json }) => {
  const activity = store.createActivity(params.id, body || {});
  json(201, ok(activity));
});

router.register('GET', '/api/activities/:id', async ({ params, json }) => {
  const activity = store.getActivity(params.id);
  if (!activity) {
    const error = new Error('Atividade não encontrada.');
    error.status = 404;
    throw error;
  }
  json(200, ok(activity));
});

router.register('PATCH', '/api/activities/:id', async ({ params, body, json }) => {
  const activity = store.updateActivity(params.id, body || {});
  json(200, ok(activity));
});

router.register('DELETE', '/api/activities/:id', async ({ params, json }) => {
  const activity = store.deleteActivity(params.id);
  json(200, ok(activity));
});

const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }

  const handled = await router.handle(req, res);
  if (!handled) {
    router.sendJson(res, 404, {
      error: {
        message: 'Rota não encontrada.',
        status: 404
      }
    });
  }
});

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`QualiFlow API disponível em http://localhost:${PORT}`);
  });
}

module.exports = server;
