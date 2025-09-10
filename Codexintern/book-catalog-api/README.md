# Book Catalog API

A RESTful API for managing a library's book catalog with CRUD operations and search functionality.

## Features

- CRUD operations for books
- Search books by title or author
- Book attributes: title, author, genre, publication year, availability
- SQLite database (can be configured for other databases)
- Flask-based REST API

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Database Setup

1. Initialize the database: `flask db init`
2. Create migration: `flask db migrate -m "Initial migration"`
3. Apply migration: `flask db upgrade`

## Running the Application

Start the development server: `python run.py`

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /api/books` - Get all books (optional query parameter `q` for search)
- `GET /api/books/<id>` - Get a specific book
- `POST /api/books` - Create a new book
- `PUT /api/books/<id>` - Update a book
- `DELETE /api/books/<id>` - Delete a book

## Testing

Run tests with: `pytest`

## Configuration

Environment variables can be set in a `.env` file:

- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection URL
- `JWT_SECRET_KEY`: JWT secret key (for future authentication)