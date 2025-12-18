# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a polyglot monorepo containing multiple personal projects, built with Bazel for multi-language support. The repository includes Python (FastAPI), Swift (macOS apps), and Go projects.

## Build System: Bazel

All projects use Bazel as the primary build system. Bazel is configured for Python 3.13, Go 1.22.2, and Swift/Apple platforms.

### Common Bazel Commands

**Building:**
```bash
# Build entire monorepo
bazel build //...

# Build specific project
bazel build //projects/concord/app:concord
bazel build //projects/budget_app:BudgetApp
bazel build //projects/bookshelf/main:bookshelf

# Build a single target
bazel build //projects/concord/app/projects:projects
```

**Testing:**
```bash
# Run all tests
bazel test //...

# Run tests for specific project
bazel test //projects/concord/tests:all
bazel test //projects/budget_app/tests:DataStoreTests

# Run single test file
bazel test //projects/concord/tests:test_projects
```

**Code Quality:**
```bash
# Auto-fix formatting and linting (runs gazelle, ruff fix, and ruff format in parallel)
bazel run //:autofix

# Regenerate BUILD files with gazelle
bazel run //:gazelle

# Format Python code with ruff
bazel run //bazel/tools:ruff-format

# Fix Python linting issues with ruff
bazel run //bazel/tools:ruff-fix
```

**Dependency Management:**
```bash
# Update Python dependencies (after modifying bazel/python/packages.in)
bazel run //bazel/python:requirements.update

# Create/update virtual environment
bazel run //:create_venv
```

## Python Development

### Python Dependencies

All Python dependencies are managed through `bazel/python/packages.in`. After modifying this file, run:
```bash
bazel run //bazel/python:requirements.update
```

This generates `bazel/python/requirements.txt` which is used by Bazel's pip integration.

### Custom Python Macros

**pytest_test**: Custom test macro that wraps py_test with pytest support
- Defined in `bazel/python/pytest/defs.bzl`
- Automatically includes pytest as a dependency
- Usage: `load("//bazel/python:defs.bzl", "pytest_test")`

**alembic**: Custom macro for Alembic database migration targets
- Defined in `bazel/python/alembic.bzl`
- Automatically includes alembic.ini configuration
- Usage: `load("//bazel/python:defs.bzl", "alembic")`

### Running Python Applications

Python applications use `__main__.py` as entry points:
```bash
# Run Concord FastAPI app
bazel run //projects/concord/app:concord

# Run Bookshelf FastAPI app
bazel run //projects/bookshelf/main:bookshelf
```

### Python Linting

Ruff is configured via `.ruff.toml` and integrated into Bazel builds. The linter runs automatically during builds and will fail on violations (configured via `--@aspect_rules_lint//lint:fail_on_violation`).

## Project Structure

### Concord (Task Management Backend)

**Location:** `projects/concord/`

**Tech Stack:** FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT authentication

**Architecture:**
- `app/api.py`: Main FastAPI application with router registration
- `app/common/`: Shared utilities (database, config, auth, models)
  - `db.py`: Database session management
  - `config.py`: Environment-based configuration
  - `oath2.py`: JWT authentication (note: typo in filename, should be oauth2)
  - `utils.py`: Password hashing/verification
  - `models.py`: SQLAlchemy database models
- `app/projects/`: Project management routes and schemas
- `app/users/`: User management routes and schemas
- `db/alembic/`: Database migrations
- `tests/`: Test suite

**Database Migrations:**
```bash
# Run migrations
bazel run //projects/concord/db:alembic -- upgrade head

# Create new migration
bazel run //projects/concord/db:alembic -- revision --autogenerate -m "description"

# Rollback migration
bazel run //projects/concord/db:alembic -- downgrade -1
```

**Environment Variables:**
- `CONCORD_DB_URL`: Database connection string
- `CONCORD_JWT_SECRET`: JWT signing secret

These are passed through Bazel via `.bazelrc`: `build --action_env=CONCORD_DB_URL`

**Key Features:**
- JWT-based authentication with OAuth2PasswordRequestForm
- SQLAlchemy ORM with relationship management
- Concurrency-safe operations with transaction isolation
- Project and task management with user assignments

### Bookshelf (Learning Project)

**Location:** `projects/bookshelf/`

**Tech Stack:** FastAPI, SQLAlchemy, SQLite

**Architecture:**
- `tutorial/`: FastAPI learning exercises
- `main/`: Main bookshelf application with CRUD operations
- `postgres/`: PostgreSQL integration examples
- `tests/`: Test suite

**Purpose:** Learning FastAPI fundamentals and database patterns before building Concord.

### Budget App (macOS Application)

**Location:** `projects/budget_app/`

**Tech Stack:** SwiftUI, Bazel (rules_swift, rules_apple)

**Architecture:**
- `app/`: SwiftUI application code
  - Models: Transaction, Category
  - Views: SwiftUI views
  - Storage: JSON-based local persistence
- `resources/`: Application resources
- `tests/`: Unit tests

**Building and Running:**
```bash
# Build the app
bazel build //projects/budget_app:BudgetApp

# Run tests
bazel test //projects/budget_app/tests:DataStoreTests
```

**Data Storage:** Stores data in `~/.budget` directory as JSON files.

### LeetCode (Algorithm Practice)

**Location:** `projects/leetcode/`

Contains Python implementations of LeetCode problems with tests.

## Development Workflow

### Adding New Python Dependencies

1. Add package to `bazel/python/packages.in`
2. Run `bazel run //bazel/python:requirements.update`
3. Run `bazel run //:gazelle` to update BUILD files
4. Commit both `packages.in` and generated `requirements.txt`

### Creating New Tests

For Python projects, use the `pytest_test` macro:
```python
load("//bazel/python:defs.bzl", "pytest_test")

pytest_test(
    name = "test_name",
    srcs = ["test_file.py"],
    deps = [
        # dependencies
    ],
)
```

### Code Formatting

Always run before committing:
```bash
bazel run //:autofix
```

This runs gazelle (BUILD file generation), ruff fix (linting), and ruff format (formatting) in parallel.

### Bazel Configuration

**`.bazelrc` settings:**
- Go race detection enabled: `--@rules_go//go/config:race`
- Python linting with ruff: `--aspects=//bazel:lint.bzl%ruff`
- Test output on errors only: `test --test_output=errors`

**Module dependencies (MODULE.bazel):**
- rules_python (1.6.3): Python toolchain
- rules_go (0.55.1): Go toolchain
- rules_swift (2.4.0) + rules_apple (3.18.0): Swift/macOS toolchain
- gazelle (0.36.0): BUILD file generation
- rules_oci (2.2.6): Container image support (postgres image for local dev)
- aspect_rules_lint (1.9.1): Linting infrastructure

## Architecture Patterns

### FastAPI Projects (Concord, Bookshelf)

**Router Pattern:**
- Main app in `api.py` or `__main__.py`
- Feature routers in subdirectories (e.g., `projects/router.py`, `users/router.py`)
- Routers included via `app.include_router()`

**Database Session Management:**
- Database sessions managed via dependency injection: `db: Session = Depends(get_db)`
- Session factory in `common/db.py`
- Connection pooling handled by SQLAlchemy

**Authentication:**
- JWT tokens created via `create_access_token()` in `common/oath2.py`
- Password hashing with bcrypt via `common/utils.py`
- OAuth2 password flow for login endpoint

**Configuration:**
- Environment variables loaded via `common/config.py`
- Settings class pattern for type-safe configuration

### Bazel Build Patterns

**Python Targets:**
- Libraries: `py_library`
- Binaries: `py_binary`
- Tests: `pytest_test` (custom macro)
- Dependencies via `requirement("package-name")` from `@pypi`

**Multi-language Support:**
- Python toolchain: 3.13
- Go toolchain: 1.22.2
- Swift toolchain: configured for macOS 13.0+

## Database Management

### Alembic Migrations (Concord)

Configuration in `alembic.ini` at repository root:
- Script location: `projects/concord/db/alembic`
- Versions directory: `projects/concord/db/alembic/versions`

Migration workflow:
1. Modify SQLAlchemy models in `app/common/models.py`
2. Generate migration: `bazel run //projects/concord/db:alembic -- revision --autogenerate -m "description"`
3. Review generated migration in `db/alembic/versions/`
4. Apply migration: `bazel run //projects/concord/db:alembic -- upgrade head`

### PostgreSQL (Concord)

Uses OCI-pulled postgres image for local development:
- Image: `arm64v8/postgres`
- Configured in MODULE.bazel under `oci.pull`

Connection managed via `CONCORD_DB_URL` environment variable.

## Important Notes

- Always run `bazel run //:autofix` before committing to ensure code quality
- Python import paths follow Bazel workspace structure (e.g., `from projects.concord.app.common.db import get_db`)
- Tests run with race detection enabled for Go code
- Linting failures will fail the build
