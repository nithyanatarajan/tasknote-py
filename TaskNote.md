# TaskNote

TaskNote is a personal productivity tool designed to manage notes and tasks with tags support. The tool also provides
insightful analytics about the user's daily activity and productivity trends.

## 1. Objectives

- Allow users to create and manage actionable items (tasks) and informational content (notes)
- Provide organising support through tagging
- Offer basic analytics to help users understand productivity habits

## 2. Target Users

- Individual users (no multi-user support initially)

## 3. Features & Functional Requirements

### Notes Service

Handles creation and management of user notes (non-actionable content).

#### APIs:

- GET /health — Health check
- POST /notes — Create a new note
- GET /notes — List all notes
- GET /notes/{id} — Get note by ID
- PUT /notes/{id} — Update a note
- DELETE /notes/{id} — Delete a note
- GET /notes/search?tag=work&text=meeting — Filter/search notes

#### Key Requirements:

- Notes should support basic text fields (title, content)
- Notes may include tags for categorization
- Notes are not time-sensitive or status-driven

### Tasks Service

Manages user tasks with priorities, deadlines, and statuses.

#### APIs:

- GET /health — Health check
- POST /tasks — Create a new task
- GET /tasks — List all tasks
- PUT /tasks/{id} — Update task (status, due date, etc.)
- DELETE /tasks/{id} — Delete task
- POST /tasks/complete/{id} — Mark task as completed
- GET /tasks/due-soon — List tasks due within next 24 hours

#### Key Requirements:

- Tasks should support status (pending, completed)
- Each task may have a due date and priority level
- Tasks can be tagged for organization

### Tagging Service

Supports categorization and filtering of notes and tasks via tags.

#### APIs:

- GET /health — Health check
- POST /tags — Create a new tag
- GET /tags — List all tags
- PUT /notes/{noteId}/tag/{tagId} — Assign tag to a note

#### Key Requirements:

- Tags are reusable across notes and tasks
- A note or task can be assigned multiple tags
- Tagging is optional but supports filtering

### Analytics Service

Generates basic user activity reports and productivity metrics.

#### APIs:

- GET /health — Health check
- GET /analytics/summary — Overall stats (e.g., completion rate, notes/tasks per day)
- GET /analytics/tasks/daily — Tasks created/completed per day
- GET /analytics/notes/daily — Notes created per day

#### Key Requirements:

- Summary includes total notes, tasks, completion rate
- Line or bar chart data for daily stats
- Data can be recalculated periodically (via batch or job)

## 4. Non-Functional Requirements

- REST APIs with consistent structure and error handling
- JSON as the data exchange format
- Microservice separation and containerization (Docker)
- Unit and integration test coverage per service
- Logging and basic monitoring (e.g., health endpoints)
- CI/CD setup (GitHub Actions, GitLab CI, etc.)

## 5. Acceptance Criteria

| Feature   | Criteria                                        |
|:----------|:------------------------------------------------|
| Notes     | Can create, edit, delete, and search notes      |
| Tasks     | Can add, complete, delete, and list tasks       |
| Tags      | Can create and assign tags                      |
| Analytics | Returns correct stats and updates with new data |

## 6. Out of Scope (for MVP)

- User authentication/multi-user support
- Sharing or collaboration features
- Rich text editing or media attachments
- Notifications/reminders (unless added later)
- User Interface via web or mobile

## 7. Tech Stack

| Category          | Tool / Library                      | Purpose                                     |
|-------------------|-------------------------------------|---------------------------------------------|
| Language          | Python 3.13                         | Core backend language                       |
| Web Framework     | FastAPI                             | Async API layer                             |
| ORM               | SQLAlchemy 2.0 (async)              | Database access abstraction                 |
| Migrations        | Alembic                             | DB versioning and schema migration          |
| Database          | PostgreSQL                          | Primary database for tasks, notes, tags     |
| API Format        | REST + JSON                         | Standard communication across services      |
| Documentation     | FastAPI auto docs (Swagger + ReDoc) | Self-updating OpenAPI docs                  |
| Health Checks     | GET /health                         | Per-service endpoint for readiness checks   |
| Config Management | Pydantic Settings                   | Type-safe `.env`-based settings             |
| Logging           | structlog                           | Zap-style structured, JSON-friendly logging |
| Linting           | ruff                                | Fast linting and formatting                 |
| Testing           | pytest + pytest-asyncio + httpx     | Async test suite + test client              |
| Dev Automation    | TaskFile                            | Task runner                                 |
| Containerization  | Docker                              | Service-level containers                    |
| CI/CD             | GitHub Actions                      | Linting, testing, Docker builds per service |
| Monitoring        | Prometheus                          | Metrics collection from services            |
| Dashboard         | Grafana                             | Visualize service-level metrics             |

