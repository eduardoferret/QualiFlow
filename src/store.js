const timestamp = () => new Date().toISOString();

class DataStore {
  constructor() {
    this.reset();
  }

  reset() {
    this.branches = new Map();
    this.sectors = new Map();
    this.users = new Map();
    this.documents = new Map();
    this.workflows = new Map();
    this.processes = new Map();
    this.activities = new Map();
    this.counters = {
      branch: 1,
      sector: 1,
      user: 1,
      document: 1,
      documentVersion: 1,
      workflow: 1,
      workflowStep: 1,
      process: 1,
      activity: 1
    };
  }

  nextId(prefix) {
    const value = this.counters[prefix] || 1;
    this.counters[prefix] = value + 1;
    return `${prefix}-${value}`;
  }

  ensure(condition, message, status = 400) {
    if (!condition) {
      const error = new Error(message);
      error.status = status;
      throw error;
    }
  }

  // Branches
  listBranches() {
    return Array.from(this.branches.values());
  }

  getBranch(id) {
    return this.branches.get(id) || null;
  }

  createBranch({ name, description = '' }) {
    this.ensure(name, 'Nome da filial é obrigatório.');
    const id = this.nextId('branch');
    const now = timestamp();
    const branch = { id, name, description, createdAt: now, updatedAt: now };
    this.branches.set(id, branch);
    return branch;
  }

  updateBranch(id, payload) {
    const current = this.getBranch(id);
    this.ensure(current, 'Filial não encontrada.', 404);
    const updated = {
      ...current,
      ...payload,
      updatedAt: timestamp()
    };
    this.branches.set(id, updated);
    return updated;
  }

  deleteBranch(id) {
    const branch = this.getBranch(id);
    this.ensure(branch, 'Filial não encontrada.', 404);
    const hasSector = Array.from(this.sectors.values()).some((sector) => sector.branchId === id);
    this.ensure(!hasSector, 'Remova ou mova os setores associados antes de excluir a filial.');
    const hasDocument = Array.from(this.documents.values()).some((doc) => doc.branchId === id);
    this.ensure(!hasDocument, 'Remova ou atualize os documentos associados antes de excluir a filial.');
    this.branches.delete(id);
    return branch;
  }

  // Sectors
  listSectors() {
    return Array.from(this.sectors.values());
  }

  getSector(id) {
    return this.sectors.get(id) || null;
  }

  createSector({ name, branchId }) {
    this.ensure(name, 'Nome do setor é obrigatório.');
    this.ensure(branchId, 'Filial associada é obrigatória.');
    this.ensure(this.branches.has(branchId), 'Filial informada não existe.');
    const id = this.nextId('sector');
    const now = timestamp();
    const sector = { id, name, branchId, createdAt: now, updatedAt: now };
    this.sectors.set(id, sector);
    return sector;
  }

  updateSector(id, payload) {
    const current = this.getSector(id);
    this.ensure(current, 'Setor não encontrado.', 404);
    if (payload.branchId) {
      this.ensure(this.branches.has(payload.branchId), 'Filial informada não existe.');
    }
    const updated = {
      ...current,
      ...payload,
      updatedAt: timestamp()
    };
    this.sectors.set(id, updated);
    return updated;
  }

  deleteSector(id) {
    const sector = this.getSector(id);
    this.ensure(sector, 'Setor não encontrado.', 404);
    const hasDocument = Array.from(this.documents.values()).some((doc) => doc.sectorId === id);
    this.ensure(!hasDocument, 'Remova ou atualize os documentos associados antes de excluir o setor.');
    this.sectors.delete(id);
    return sector;
  }

  // Users
  listUsers() {
    return Array.from(this.users.values());
  }

  getUser(id) {
    return this.users.get(id) || null;
  }

  createUser({ name, email, role = 'colaborador' }) {
    this.ensure(name, 'Nome do usuário é obrigatório.');
    this.ensure(email, 'Email do usuário é obrigatório.');
    const id = this.nextId('user');
    const now = timestamp();
    const user = { id, name, email, role, createdAt: now, updatedAt: now };
    this.users.set(id, user);
    return user;
  }

  updateUser(id, payload) {
    const current = this.getUser(id);
    this.ensure(current, 'Usuário não encontrado.', 404);
    const updated = {
      ...current,
      ...payload,
      updatedAt: timestamp()
    };
    this.users.set(id, updated);
    return updated;
  }

  deleteUser(id) {
    const user = this.getUser(id);
    this.ensure(user, 'Usuário não encontrado.', 404);
    const assigned = Array.from(this.activities.values()).some((activity) => activity.assignedTo === id);
    this.ensure(!assigned, 'Não é possível excluir usuários vinculados a atividades.');
    this.users.delete(id);
    return user;
  }

  // Documents
  listDocuments() {
    return Array.from(this.documents.values());
  }

  getDocument(id) {
    return this.documents.get(id) || null;
  }

  createDocument({ title, description = '', branchId, sectorId = null, fileName = null, fileUrl = null }) {
    this.ensure(title, 'Título do documento é obrigatório.');
    this.ensure(branchId, 'Filial do documento é obrigatória.');
    this.ensure(this.branches.has(branchId), 'Filial informada não existe.');
    if (sectorId) {
      this.ensure(this.sectors.has(sectorId), 'Setor informado não existe.');
    }
    const id = this.nextId('document');
    const now = timestamp();
    const document = {
      id,
      title,
      description,
      branchId,
      sectorId,
      versions: [],
      createdAt: now,
      updatedAt: now
    };
    this.documents.set(id, document);
    if (fileName || fileUrl) {
      this.addDocumentVersion(id, { fileName, fileUrl, notes: 'Versão inicial.' });
    }
    return this.getDocument(id);
  }

  addDocumentVersion(documentId, { fileName = null, fileUrl = null, notes = '' }) {
    const document = this.getDocument(documentId);
    this.ensure(document, 'Documento não encontrado.', 404);
    const versionNumber = document.versions.length + 1;
    const versionId = this.nextId('documentVersion');
    const now = timestamp();
    const version = {
      id: versionId,
      version: versionNumber,
      fileName,
      fileUrl,
      notes,
      createdAt: now
    };
    document.versions.push(version);
    document.updatedAt = now;
    return version;
  }

  updateDocument(id, payload) {
    const document = this.getDocument(id);
    this.ensure(document, 'Documento não encontrado.', 404);
    if (payload.branchId) {
      this.ensure(this.branches.has(payload.branchId), 'Filial informada não existe.');
    }
    if (payload.sectorId) {
      this.ensure(this.sectors.has(payload.sectorId), 'Setor informado não existe.');
    }
    const updated = {
      ...document,
      ...payload,
      updatedAt: timestamp()
    };
    // preserve versions array separately to avoid overwriting when payload doesn't include
    if (!payload.versions) {
      updated.versions = document.versions;
    }
    this.documents.set(id, updated);
    return updated;
  }

  deleteDocument(id) {
    const document = this.getDocument(id);
    this.ensure(document, 'Documento não encontrado.', 404);
    const referenced = Array.from(this.processes.values()).some((process) => (process.documentIds || []).includes(id));
    this.ensure(!referenced, 'Documento associado a processos não pode ser excluído.');
    this.documents.delete(id);
    return document;
  }

  // Workflows
  listWorkflows() {
    return Array.from(this.workflows.values());
  }

  getWorkflow(id) {
    return this.workflows.get(id) || null;
  }

  createWorkflow({ name, description = '', steps = [] }) {
    this.ensure(name, 'Nome do fluxo de trabalho é obrigatório.');
    const id = this.nextId('workflow');
    const now = timestamp();
    const normalizedSteps = steps.map((step, index) => this.normalizeWorkflowStep(step, index + 1));
    const workflow = {
      id,
      name,
      description,
      steps: normalizedSteps,
      createdAt: now,
      updatedAt: now
    };
    this.workflows.set(id, workflow);
    return workflow;
  }

  normalizeWorkflowStep(step, order) {
    const id = this.nextId('workflowStep');
    return {
      id,
      name: step.name || `Etapa ${order}`,
      description: step.description || '',
      order
    };
  }

  updateWorkflow(id, payload) {
    const workflow = this.getWorkflow(id);
    this.ensure(workflow, 'Fluxo de trabalho não encontrado.', 404);
    let steps = workflow.steps;
    if (Array.isArray(payload.steps)) {
      steps = payload.steps.map((step, index) => this.normalizeWorkflowStep(step, index + 1));
    }
    const updated = {
      ...workflow,
      ...payload,
      steps,
      updatedAt: timestamp()
    };
    this.workflows.set(id, updated);
    return updated;
  }

  deleteWorkflow(id) {
    const workflow = this.getWorkflow(id);
    this.ensure(workflow, 'Fluxo de trabalho não encontrado.', 404);
    const inUse = Array.from(this.processes.values()).some((process) => process.workflowId === id);
    this.ensure(!inUse, 'Fluxo utilizado por processos ativos não pode ser excluído.');
    this.workflows.delete(id);
    return workflow;
  }

  // Processes
  listProcesses() {
    return Array.from(this.processes.values());
  }

  getProcess(id) {
    return this.processes.get(id) || null;
  }

  createProcess({ name, description = '', workflowId, ownerId = null, documentIds = [] }) {
    this.ensure(name, 'Nome do processo é obrigatório.');
    this.ensure(workflowId, 'Fluxo de trabalho associado é obrigatório.');
    const workflow = this.getWorkflow(workflowId);
    this.ensure(workflow, 'Fluxo de trabalho informado não existe.');
    if (ownerId) {
      this.ensure(this.users.has(ownerId), 'Responsável informado não existe.');
    }
    const invalidDocument = documentIds.find((docId) => !this.documents.has(docId));
    this.ensure(!invalidDocument, `Documento ${invalidDocument} não encontrado.`);
    const id = this.nextId('process');
    const now = timestamp();
    const process = {
      id,
      name,
      description,
      workflowId,
      ownerId,
      documentIds,
      status: workflow.steps.length ? 'pendente' : 'concluido',
      currentStepIndex: 0,
      history: [],
      createdAt: now,
      updatedAt: now
    };
    this.processes.set(id, process);
    return process;
  }

  advanceProcess(id, { notes = '', performedBy = null } = {}) {
    const process = this.getProcess(id);
    this.ensure(process, 'Processo não encontrado.', 404);
    const workflow = this.getWorkflow(process.workflowId);
    this.ensure(workflow, 'Fluxo de trabalho do processo não encontrado.');
    this.ensure(process.currentStepIndex < workflow.steps.length, 'Processo já foi concluído.');
    const step = workflow.steps[process.currentStepIndex];
    const entry = {
      stepId: step.id,
      stepName: step.name,
      notes,
      performedBy,
      completedAt: timestamp()
    };
    process.history.push(entry);
    process.currentStepIndex += 1;
    process.status = process.currentStepIndex >= workflow.steps.length ? 'concluido' : 'em_andamento';
    process.updatedAt = entry.completedAt;
    return process;
  }

  updateProcess(id, payload) {
    const process = this.getProcess(id);
    this.ensure(process, 'Processo não encontrado.', 404);
    if (payload.workflowId && payload.workflowId !== process.workflowId) {
      this.ensure(false, 'Não é permitido alterar o fluxo de um processo em andamento.');
    }
    if (payload.ownerId) {
      this.ensure(this.users.has(payload.ownerId), 'Responsável informado não existe.');
    }
    if (payload.documentIds) {
      payload.documentIds.forEach((docId) => {
        this.ensure(this.documents.has(docId), `Documento ${docId} não encontrado.`);
      });
    }
    const updated = {
      ...process,
      ...payload,
      updatedAt: timestamp()
    };
    this.processes.set(id, updated);
    return updated;
  }

  deleteProcess(id) {
    const process = this.getProcess(id);
    this.ensure(process, 'Processo não encontrado.', 404);
    const hasActivities = Array.from(this.activities.values()).some((activity) => activity.processId === id);
    this.ensure(!hasActivities, 'Processo com atividades não pode ser excluído.');
    this.processes.delete(id);
    return process;
  }

  // Activities
  listActivities(filter = {}) {
    const { processId = null, status = null } = filter;
    return Array.from(this.activities.values()).filter((activity) => {
      if (processId && activity.processId !== processId) {
        return false;
      }
      if (status && activity.status !== status) {
        return false;
      }
      return true;
    });
  }

  getActivity(id) {
    return this.activities.get(id) || null;
  }

  createActivity(processId, { title, description = '', assignedTo = null, dueDate = null }) {
    this.ensure(processId, 'Processo associado é obrigatório.');
    const process = this.getProcess(processId);
    this.ensure(process, 'Processo não encontrado.', 404);
    this.ensure(title, 'Título da atividade é obrigatório.');
    if (assignedTo) {
      this.ensure(this.users.has(assignedTo), 'Usuário responsável não existe.');
    }
    const id = this.nextId('activity');
    const now = timestamp();
    const activity = {
      id,
      processId,
      title,
      description,
      assignedTo,
      dueDate,
      status: 'pendente',
      createdAt: now,
      updatedAt: now
    };
    this.activities.set(id, activity);
    return activity;
  }

  updateActivity(id, payload) {
    const activity = this.getActivity(id);
    this.ensure(activity, 'Atividade não encontrada.', 404);
    if (payload.assignedTo) {
      this.ensure(this.users.has(payload.assignedTo), 'Usuário responsável não existe.');
    }
    const updated = {
      ...activity,
      ...payload,
      updatedAt: timestamp()
    };
    this.activities.set(id, updated);
    return updated;
  }

  deleteActivity(id) {
    const activity = this.getActivity(id);
    this.ensure(activity, 'Atividade não encontrada.', 404);
    this.activities.delete(id);
    return activity;
  }
}

module.exports = new DataStore();
