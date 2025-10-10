# 🧩 Concord — Collaborative Task Board (Backend Focus)

**Goal:** Build a real-time collaborative task board backend (like Trello + Notion-lite) using **FastAPI**, **Postgres**, **SQLModel**, and **Alembic**.  
This project doubles as a **4-day intensive study plan** leading up to a backend interview on **Monday, Oct 13**.  
By the end, you'll be confident in **Python backend development**, **Postgres schema design**, **normalization**, **concurrency**, and **locking**.

---

## 🚀 Project Overview

**Concord** is a backend system where multiple users can collaborate on boards, lists, and tasks — safely handling **concurrent edits** and **transactions** at both the application and database level.

### 🔧 Tech Stack
- **FastAPI** — async backend framework  
- **SQLModel** — ORM layer (built on SQLAlchemy)  
- **PostgreSQL** — relational database  
- **Alembic** — schema migrations  
- *(Optional later)* Redis for pub/sub or async locking  

### 🧠 Key Concepts Covered
- Async I/O with FastAPI (`async def`, background tasks)
- SQLModel sessions and dependency injection
- Alembic migrations and schema evolution
- Postgres MVCC (Multi-Version Concurrency Control)
- Isolation levels & row-level locking (`SELECT FOR UPDATE`)
- Optimistic vs pessimistic concurrency control
- Schema normalization (1NF–3NF)
- Indexing, foreign keys, and query optimization

---

## 🗓️ Study Plan (Oct 9 → Oct 12)

### **Day 1 — Backend Foundations**
**Theme:** Get comfortable with FastAPI & database plumbing.

#### 🎯 Objectives
- Set up the `Concord` project scaffold
- Understand FastAPI request handling and dependency injection
- Learn SQLModel and Alembic basics

#### 🧩 Tasks
1. Watch → [FastAPI Crash Course (freeCodeCamp)](https://www.youtube.com/watch?v=0sOvCWFmrtA)  
2. Implement:
   - `main.py`
   - `models.py`
   - `database.py`
   - Basic `/boards` CRUD routes  
3. Initialize Alembic and run your first migration (`alembic revision --autogenerate -m "init"`)

#### 🧠 Concepts
- Async endpoints vs sync
- Session lifecycles (`autocommit`, `autoflush`)
- How FastAPI injects dependencies

#### ✅ Product Checkpoint
- You can **start the FastAPI server (`uvicorn app.main:app --reload`)**  
- `/boards` CRUD routes are working end-to-end (create, list, delete)  
- Postgres connection + Alembic migrations verified  
- Project structure initialized and committed  

---

### **Day 2 — Schema Design & Normalization**
**Theme:** Think in relations.

#### 🎯 Objectives
- Design normalized schemas for `Board`, `TaskList`, and `Task`
- Learn foreign keys, indexes, and migration strategy

#### 🧩 Tasks
1. Watch → [Database Design Full Course (freeCodeCamp)](https://www.youtube.com/watch?v=ztHopE5Wnpc)  
2. Implement schema models + relationships in SQLModel  
3. Run and inspect migrations  
4. Use `EXPLAIN` to understand query plans  

#### 🧠 Concepts
- 1NF → 3NF normalization  
- Indexing (`CREATE INDEX`, composite, unique)
- Foreign keys & referential integrity
- When to denormalize for performance

#### ✅ Product Checkpoint
- Schema defined for **Board → List → Task** relationships  
- Alembic migration successfully generated and applied  
- Verified foreign keys and indexes exist in Postgres (`\d+ table_name`)  
- `GET /boards/{id}/lists` and `GET /lists/{id}/tasks` routes return relational data  
- Documented ERD (text-based or diagram) checked in  

---

### **Day 3 — Concurrency & Transactions**
**Theme:** Master Postgres MVCC and async concurrency.

#### 🎯 Objectives
- Explore isolation levels and row locks
- Implement optimistic & pessimistic concurrency control
- Simulate concurrent writes from Python

#### 🧩 Tasks
1. Watch → “PostgreSQL Transactions & Isolation Levels Explained” (NeuralNine / DataEngCourses)  
2. Add endpoints:
   - `/tasks/{id}/assign` — uses `SELECT FOR UPDATE`
   - `/tasks/{id}/update` — checks `version` field  
3. Write a concurrency demo using `asyncio.gather()` to simulate race conditions  
4. Log and analyze behavior under different isolation levels  

#### 🧠 Concepts
- MVCC visibility and snapshots  
- `SELECT FOR UPDATE`, `NOWAIT`, and advisory locks  
- `SERIALIZABLE` vs `READ COMMITTED`  
- Connection pooling & async session handling

#### ✅ Product Checkpoint
- `/tasks/{id}/assign` endpoint correctly serializes concurrent requests  
- Versioned task updates prevent stale writes (returns `409 Conflict` on mismatch)  
- `concurrency_demo.py` script shows expected lock behavior when run concurrently  
- Documented results: timing logs, conflict outcomes, isolation-level notes  

---

### **Day 4 — Polish & Interview Drills**
**Theme:** Tie it all together and prepare to explain it.

#### 🎯 Objectives
- Add background tasks and error handling
- Review and rehearse architecture & schema discussions

#### 🧩 Tasks
1. Implement activity logging using FastAPI `BackgroundTasks`  
2. Run concurrent simulations and capture logs  
3. Practice interview answers:
   - “Explain your backend architecture”
   - “How do you handle concurrency?”
   - “How do you design scalable schemas?”  

#### 🧠 Concepts
- ACID in Postgres  
- Async concurrency vs DB concurrency  
- Migration/versioning workflow (Alembic)  
- Trade-offs between isolation and throughput

#### ✅ Product Checkpoint
- Background task logging integrated into task updates  
- Error handling with proper HTTP codes (`400`, `409`, `500`)  
- Logs and concurrency traces stored in `/logs/` directory  
- Short architecture summary written in `ARCHITECTURE.md`  
- End-to-end demo (from creating a board to concurrent updates) runs cleanly  

---

## ✅ Final Deliverables (by Oct 12)
- ✅ Fully running FastAPI server (`uvicorn main:app --reload`)
- ✅ Connected Postgres DB with Alembic migrations
- ✅ CRUD + concurrency-safe endpoints
- ✅ Documented notes on:
  - Schema design & normalization
  - Locking mechanisms used
  - Isolation-level behavior observed
