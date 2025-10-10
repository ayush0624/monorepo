# ✅ Concord — Personal Linear-Style Task Management Backend

**Goal:** Build a high-performance backend for managing your everyday tasks and projects — inspired by **Linear**, but built from scratch using **FastAPI**, **Postgres**, **SQLModel**, and **Alembic**.  

---

## 🚀 Project Overview

**Concord** is a minimal but powerful task management system — a backend that models how you actually work day-to-day.  
You’ll be able to create projects, tasks, tags, and track progress with concurrency-safe updates and transactional consistency.

Imagine Linear or Todoist — but entirely self-hosted and optimized for developer workflows.

---

### 🔧 Tech Stack
- **FastAPI** — async backend framework  
- **SQLModel** — ORM layer (built on SQLAlchemy)  
- **PostgreSQL** — relational database  
- **Alembic** — schema migrations  
- *(Optional later)* Redis for async background jobs and distributed locks  

---

### 🧠 Core Concepts
- Async I/O and background tasks with FastAPI  
- SQLModel + Alembic for schema design and migrations  
- MVCC (Multi-Version Concurrency Control) and transaction isolation  
- Optimistic vs pessimistic concurrency control  
- Schema normalization and indexing for performance  

---

## 🗓️ Study Plan (Oct 9 → Oct 12)

### **Day 1 — Backend Foundations**
**Theme:** Get comfortable with FastAPI & database plumbing.

#### 🎯 Objectives
- Scaffold the `Concord` project
- Understand FastAPI’s dependency injection and async lifecycle
- Set up database and migrations

#### 🧩 Tasks
1. Watch → [FastAPI Crash Course (freeCodeCamp)](https://www.youtube.com/watch?v=0sOvCWFmrtA)
2. Implement:
   - `main.py`
   - `models.py`
   - `database.py`
   - Basic `/projects` CRUD routes
3. Initialize Alembic and run your first migration

#### 🧠 Concepts
- Async endpoints vs sync
- Dependency injection for DB sessions
- SQLModel base setup and Alembic integration

#### ✅ Product Checkpoint
- FastAPI server starts successfully (`uvicorn app.main:app --reload`)  
- `/projects` CRUD endpoints work  
- Database tables created via Alembic  
- Commit: `feat(day1): setup base project + project CRUD`

---

### **Day 2 — Schema Design & Normalization**
**Theme:** Think in relations.

#### 🎯 Objectives
- Design normalized schemas for Projects, Tasks, and Tags
- Implement relationships and indexing

#### 🧩 Tasks
1. Watch → [Database Design Full Course (freeCodeCamp)](https://www.youtube.com/watch?v=ztHopE5Wnpc)
2. Define models:
   - `Project`: name, description
   - `Task`: title, status, due_date, project_id
   - `Tag`: name (many-to-many with Task)
3. Write Alembic migrations and validate schema
4. Run a few example queries with `EXPLAIN`

#### 🧠 Concepts
- 1NF → 3NF normalization  
- Composite keys and foreign keys  
- Query planning and index usage  

#### ✅ Product Checkpoint
- Fully normalized schema for projects, tasks, and tags  
- `/tasks` routes working with filtering by project or tag  
- `alembic revision --autogenerate` produces valid SQL  
- Commit: `feat(day2): add task + tag models with migrations`

---

### **Day 3 — Concurrency & Transactions**
**Theme:** Ensure correctness under concurrent updates.

#### 🎯 Objectives
- Add endpoints for task assignment and status changes
- Implement optimistic and pessimistic concurrency control
- Simulate concurrent updates using `asyncio.gather`

#### 🧩 Tasks
1. Watch → “PostgreSQL Transactions & Isolation Levels Explained”  
2. Add endpoints:
   - `/tasks/{id}/assign` → lock row with `SELECT FOR UPDATE`
   - `/tasks/{id}/update` → optimistic concurrency check on version
3. Create `concurrency_demo.py` to simulate race conditions
4. Log outcomes and analyze conflicts

#### 🧠 Concepts
- MVCC, snapshots, visibility
- Locking strategies: `FOR UPDATE`, `NOWAIT`, advisory locks
- Versioned updates for conflict prevention  

#### ✅ Product Checkpoint
- Concurrency demo shows correct locking behavior  
- Task updates prevent stale writes (`409 Conflict`)  
- Logs show transaction timing and outcomes  
- Commit: `feat(day3): implement concurrency control + demo`

---

### **Day 4 — Polish & Interview Drills**
**Theme:** Tie it all together and prepare to explain it.

#### 🎯 Objectives
- Add background logging and better error handling
- Review your system architecture and practice explaining it

#### 🧩 Tasks
1. Add background activity logging (FastAPI `BackgroundTasks`)
2. Add proper error handling and response models
3. Create `ARCHITECTURE.md` summarizing design choices
4. Practice interview explanations:
   - “How does your backend handle concurrency?”
   - “How does MVCC work in Postgres?”
   - “How do you design scalable schemas?”

#### 🧠 Concepts
- ACID transactions
- Async background tasks vs database transactions
- Alembic migrations in CI/CD pipelines  

#### ✅ Product Checkpoint
- Background logging integrated  
- `/tasks` endpoint responses validated  
- Architecture document written  
- Full workflow demo: create → assign → update → complete  
- Commit: `feat(day4): finalize concurrency-safe backend + docs`

---

## ✅ Final Deliverables (by Oct 12)
- Fully working FastAPI + Postgres backend
- CRUD and concurrency-safe endpoints
- Structured schema with migrations
- Architecture and concurrency notes
- Local concurrency demo script
