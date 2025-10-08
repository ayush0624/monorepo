import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from projects.bookshelf.main.api import app
from projects.bookshelf.main.db import Base, get_db

# Create a test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override the get_db dependency to use the test database."""
    db = TestSessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create and drop test database tables for each test."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database dependency."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestPingEndpoint:
    """Tests for the /ping endpoint."""

    def test_ping_returns_pong(self, client):
        """Test that ping endpoint returns correct response."""
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}


class TestGetAllBooks:
    """Tests for GET /books/ endpoint."""

    def test_get_all_books_empty(self, client):
        """Test getting all books when database is empty."""
        response = client.get("/books/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_books_with_data(self, client):
        """Test getting all books when database has books."""
        # Create some books
        book1 = {"name": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
        book2 = {"name": "1984", "author": "George Orwell"}

        client.post("/books/", json=book1)
        client.post("/books/", json=book2)

        # Get all books
        response = client.get("/books/")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2
        assert books[0]["name"] == "The Great Gatsby"
        assert books[0]["author"] == "F. Scott Fitzgerald"
        assert books[1]["name"] == "1984"
        assert books[1]["author"] == "George Orwell"


class TestGetBookById:
    """Tests for GET /books/{id} endpoint."""

    def test_get_book_by_id_success(self, client):
        """Test getting a book by ID when it exists."""
        # Create a book
        book_data = {"name": "To Kill a Mockingbird", "author": "Harper Lee"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Get the book by ID
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "To Kill a Mockingbird"
        assert response.json()["author"] == "Harper Lee"
        assert response.json()["id"] == book_id

    def test_get_book_by_id_not_found(self, client):
        """Test getting a book by ID when it doesn't exist."""
        # Try to get a book with non-existent ID
        response = client.get("/books/999")
        assert response.status_code == 404
        assert response.json()["error"] == "EntityDoesNotExistError"


class TestCreateBook:
    """Tests for POST /books/ endpoint."""

    def test_create_book_success(self, client):
        """Test creating a new book successfully."""
        book_data = {"name": "Pride and Prejudice", "author": "Jane Austen"}
        response = client.post("/books/", json=book_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pride and Prejudice"
        assert data["author"] == "Jane Austen"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_book_missing_name(self, client):
        """Test creating a book without required name field."""
        book_data = {"author": "Jane Austen"}
        response = client.post("/books/", json=book_data)
        assert response.status_code == 422  # Validation error

    def test_create_book_missing_author(self, client):
        """Test creating a book without required author field."""
        book_data = {"name": "Pride and Prejudice"}
        response = client.post("/books/", json=book_data)
        assert response.status_code == 422  # Validation error

    def test_create_multiple_books(self, client):
        """Test creating multiple books and verify they get unique IDs."""
        book1 = {"name": "Book 1", "author": "Author 1"}
        book2 = {"name": "Book 2", "author": "Author 2"}

        response1 = client.post("/books/", json=book1)
        response2 = client.post("/books/", json=book2)

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["id"] != response2.json()["id"]


class TestUpdateBook:
    """Tests for PUT /books/{id} endpoint."""

    def test_update_book_name_only(self, client):
        """Test updating only the name of a book."""
        # Create a book
        book_data = {"name": "Original Name", "author": "Original Author"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Update only the name
        update_data = {"name": "Updated Name"}
        response = client.put(f"/books/{book_id}", json=update_data)

        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["name"] == "Updated Name"
        assert updated_book["author"] == "Original Author"
        assert updated_book["id"] == book_id

    def test_update_book_author_only(self, client):
        """Test updating only the author of a book."""
        # Create a book
        book_data = {"name": "Original Name", "author": "Original Author"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Update only the author
        update_data = {"author": "Updated Author"}
        response = client.put(f"/books/{book_id}", json=update_data)

        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["name"] == "Original Name"
        assert updated_book["author"] == "Updated Author"
        assert updated_book["id"] == book_id

    def test_update_book_both_fields(self, client):
        """Test updating both name and author of a book."""
        # Create a book
        book_data = {"name": "Original Name", "author": "Original Author"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Update both fields
        update_data = {"name": "Updated Name", "author": "Updated Author"}
        response = client.put(f"/books/{book_id}", json=update_data)

        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["name"] == "Updated Name"
        assert updated_book["author"] == "Updated Author"
        assert updated_book["id"] == book_id

    def test_update_book_not_found(self, client):
        """Test updating a book that doesn't exist."""
        update_data = {"name": "Updated Name"}
        response = client.put("/books/999", json=update_data)
        assert response.status_code == 404
        assert response.json()["error"] == "EntityDoesNotExistError"

    def test_update_book_no_changes(self, client):
        """Test updating a book with empty update data."""
        # Create a book
        book_data = {"name": "Original Name", "author": "Original Author"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Update with no changes
        update_data = {}
        response = client.put(f"/books/{book_id}", json=update_data)

        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["name"] == "Original Name"
        assert updated_book["author"] == "Original Author"


class TestDeleteBook:
    """Tests for DELETE /books/{id} endpoint."""

    def test_delete_book_success(self, client):
        """Test deleting a book successfully."""
        # Create a book
        book_data = {"name": "Book to Delete", "author": "Some Author"}
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]

        # Delete the book
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 200
        deleted_book = response.json()
        assert deleted_book["id"] == book_id
        assert deleted_book["name"] == "Book to Delete"

        # Verify the book is actually deleted
        get_response = client.get(f"/books/{book_id}")
        assert response.status_code == 404
        assert response.json()["error"] == "EntityDoesNotExistError"

    def test_delete_book_not_found(self, client):
        """Test deleting a book that doesn't exist."""
        response = client.delete("/books/999")
        assert response.status_code == 404
        assert response.json()["error"] == "EntityDoesNotExistError"

    def test_delete_book_verify_list(self, client):
        """Test that deleted book is removed from the list."""
        # Create two books
        book1 = {"name": "Book 1", "author": "Author 1"}
        book2 = {"name": "Book 2", "author": "Author 2"}

        response1 = client.post("/books/", json=book1)
        response2 = client.post("/books/", json=book2)
        book1_id = response1.json()["id"]

        # Delete the first book
        client.delete(f"/books/{book1_id}")

        # Get all books
        all_books_response = client.get("/books/")
        books = all_books_response.json()

        assert len(books) == 1
        assert books[0]["name"] == "Book 2"
