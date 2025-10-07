# Bookshelf API

A FastAPI-based bookshelf management system with full CRUD operations.

## Project Structure

- **tutorial/**: Learning materials and exercises covering FastAPI fundamentals before implementing the main bookshelf application
- **main/**: Main application code (to be implemented)

## Features

- **CRUD Endpoints**: Create, Read, Update, and Delete books
- **SQLite Backend**: Lightweight database for persistent storage
- **Dependency Injection**: Uses FastAPI's `Depends(get_db)` pattern for database session management

## API Endpoints

- `POST /books` - Create a new book
- `GET /books` - List all books
- `GET /books/{id}` - Get a specific book by ID
- `PUT /books/{id}` - Update a book
- `DELETE /books/{id}` - Delete a book

## Architecture

- **Database**: SQLite with SQLAlchemy ORM
- **Dependency Injection**: Database sessions managed through FastAPI's dependency injection system
- **Models**: SQLAlchemy models for book entities
- **Schemas**: Pydantic models for request/response validation
