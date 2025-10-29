"""QualiFlow simplified quality management application.

This module provides in-memory models that emulate the core
functionalities requested for the QualiFlow system:

* Document management with uploads and versioning.
* Workflow definition for process steps.
* Process creation bound to a workflow lifecycle.
* Activity and task management to support project execution.
* Organizational hierarchy with users, branches and sectors.

The script exposes a tiny CLI demo that instantiates the core
entities and prints a summary report.  The implementation is
self-contained and does not rely on Django so it can be executed
standalone while the full web system is being developed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class Branch:
    """Represents a company branch (filial)."""

    name: str
    address: str
    sectors: List["Sector"] = field(default_factory=list)

    def add_sector(self, sector: "Sector") -> None:
        if sector not in self.sectors:
            self.sectors.append(sector)
            sector.branch = self


@dataclass
class Sector:
    """Represents a company sector (department)."""

    name: str
    branch: Optional[Branch] = None


@dataclass
class User:
    """Simple user representation."""

    username: str
    email: str
    sector: Optional[Sector] = None


@dataclass
class DocumentVersion:
    """A specific version of a document."""

    version: int
    uploaded_by: User
    uploaded_at: datetime
    file_path: Path


@dataclass
class Document:
    """Document with versioning support."""

    title: str
    description: str
    versions: List[DocumentVersion] = field(default_factory=list)

    def add_version(self, file_path: Path, uploaded_by: User) -> DocumentVersion:
        version_number = len(self.versions) + 1
        version = DocumentVersion(
            version=version_number,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.utcnow(),
            file_path=file_path,
        )
        self.versions.append(version)
        return version

    @property
    def latest_version(self) -> Optional[DocumentVersion]:
        return self.versions[-1] if self.versions else None


@dataclass
class WorkflowStep:
    """A single step in a workflow."""

    name: str
    order: int
    description: str = ""


@dataclass
class Workflow:
    """Workflow definition used by processes."""

    name: str
    steps: List[WorkflowStep] = field(default_factory=list)

    def add_step(self, name: str, description: str = "") -> WorkflowStep:
        step = WorkflowStep(name=name, order=len(self.steps) + 1, description=description)
        self.steps.append(step)
        return step

    def get_step(self, order: int) -> WorkflowStep:
        for step in self.steps:
            if step.order == order:
                return step
        raise ValueError(f"No step with order {order} in workflow {self.name}")


@dataclass
class ProcessStage:
    """Represents a process stage mapped to a workflow step."""

    step: WorkflowStep
    completed: bool = False
    completed_at: Optional[datetime] = None

    def mark_complete(self) -> None:
        self.completed = True
        self.completed_at = datetime.utcnow()


@dataclass
class Process:
    """Process instance that follows a workflow."""

    name: str
    workflow: Workflow
    stages: List[ProcessStage] = field(init=False)

    def __post_init__(self) -> None:
        self.stages = [ProcessStage(step=step) for step in self.workflow.steps]

    def advance(self, order: int) -> None:
        stage = self.stages[order - 1]
        stage.mark_complete()

    @property
    def progress(self) -> float:
        if not self.stages:
            return 0.0
        completed = sum(1 for stage in self.stages if stage.completed)
        return completed / len(self.stages)


@dataclass
class Task:
    """Individual task inside an activity."""

    title: str
    assignee: Optional[User]
    due_date: Optional[datetime] = None
    completed: bool = False

    def mark_done(self) -> None:
        self.completed = True


@dataclass
class Activity:
    """Activity container for project work."""

    name: str
    owner: User
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, title: str, assignee: Optional[User] = None, due_date: Optional[datetime] = None) -> Task:
        task = Task(title=title, assignee=assignee, due_date=due_date)
        self.tasks.append(task)
        return task

    @property
    def completed_tasks(self) -> Iterable[Task]:
        return (task for task in self.tasks if task.completed)

    @property
    def pending_tasks(self) -> Iterable[Task]:
        return (task for task in self.tasks if not task.completed)


class QualityManagementSystem:
    """Facade that aggregates the various modules."""

    def __init__(self) -> None:
        self.branches: Dict[str, Branch] = {}
        self.users: Dict[str, User] = {}
        self.documents: Dict[str, Document] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.processes: Dict[str, Process] = {}
        self.activities: Dict[str, Activity] = {}

    # --- branch and sector management -------------------------------------------------
    def create_branch(self, name: str, address: str) -> Branch:
        branch = Branch(name=name, address=address)
        self.branches[name] = branch
        return branch

    def create_sector(self, name: str, branch_name: str) -> Sector:
        branch = self.branches[branch_name]
        sector = Sector(name=name, branch=branch)
        branch.add_sector(sector)
        return sector

    # --- user management ---------------------------------------------------------------
    def create_user(self, username: str, email: str, sector: Optional[Sector] = None) -> User:
        user = User(username=username, email=email, sector=sector)
        self.users[username] = user
        return user

    # --- document module ---------------------------------------------------------------
    def create_document(self, title: str, description: str) -> Document:
        document = Document(title=title, description=description)
        self.documents[title] = document
        return document

    # --- workflow module ---------------------------------------------------------------
    def create_workflow(self, name: str, steps: List[str]) -> Workflow:
        workflow = Workflow(name=name)
        for step_name in steps:
            workflow.add_step(step_name)
        self.workflows[name] = workflow
        return workflow

    # --- process module ----------------------------------------------------------------
    def create_process(self, name: str, workflow_name: str) -> Process:
        workflow = self.workflows[workflow_name]
        process = Process(name=name, workflow=workflow)
        self.processes[name] = process
        return process

    # --- activity module ---------------------------------------------------------------
    def create_activity(self, name: str, owner_username: str) -> Activity:
        owner = self.users[owner_username]
        activity = Activity(name=name, owner=owner)
        self.activities[name] = activity
        return activity

    # --- reporting ---------------------------------------------------------------------
    def describe(self) -> str:
        lines = ["===== QualiFlow Snapshot ====="]

        lines.append("-- Branches and Sectors --")
        for branch in self.branches.values():
            sectors = ", ".join(sector.name for sector in branch.sectors) or "(sem setores)"
            lines.append(f" * {branch.name} ({branch.address}) -> {sectors}")

        lines.append("\n-- Documents --")
        for document in self.documents.values():
            latest = document.latest_version
            if latest:
                info = f"v{latest.version} por {latest.uploaded_by.username} em {latest.uploaded_at:%Y-%m-%d %H:%M}"
            else:
                info = "sem versões"
            lines.append(f" * {document.title}: {info}")

        lines.append("\n-- Workflows --")
        for workflow in self.workflows.values():
            steps = ", ".join(step.name for step in workflow.steps) or "(sem etapas)"
            lines.append(f" * {workflow.name}: {steps}")

        lines.append("\n-- Processes --")
        for process in self.processes.values():
            progress = f"{process.progress:.0%}"
            lines.append(f" * {process.name}: {progress} concluído")

        lines.append("\n-- Activities --")
        for activity in self.activities.values():
            completed = sum(1 for _ in activity.completed_tasks)
            pending = sum(1 for _ in activity.pending_tasks)
            lines.append(f" * {activity.name}: {completed} concluídas, {pending} pendentes")

        return "\n".join(lines)


def demo() -> None:
    """Run a minimal demonstration of the system."""

    system = QualityManagementSystem()

    # Organization setup
    branch = system.create_branch("Matriz", "Av. Central, 100")
    sector_quality = system.create_sector("Qualidade", branch.name)
    sector_it = system.create_sector("Tecnologia", branch.name)

    user_ana = system.create_user("ana", "ana@example.com", sector_quality)
    user_bruno = system.create_user("bruno", "bruno@example.com", sector_it)

    # Document management
    policy_doc = system.create_document("Política de Qualidade", "Documento mestre da qualidade")
    policy_doc.add_version(Path("docs/politica_v1.pdf"), uploaded_by=user_ana)
    policy_doc.add_version(Path("docs/politica_v2.pdf"), uploaded_by=user_ana)

    # Workflow and process
    workflow = system.create_workflow("Implantação", ["Planejamento", "Execução", "Revisão"])
    process = system.create_process("Projeto X", workflow.name)
    process.advance(1)

    # Activity management
    activity = system.create_activity("Projeto X - Sprint 1", owner_username=user_bruno.username)
    task1 = activity.add_task("Configurar ambiente", assignee=user_bruno)
    task1.mark_done()
    activity.add_task("Coletar requisitos", assignee=user_ana)

    print(system.describe())


if __name__ == "__main__":
    demo()
