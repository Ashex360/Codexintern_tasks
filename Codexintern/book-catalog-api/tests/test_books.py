import pytest
import json
from app.models import Book

def test_get_all_books(test_client, init_database, auth_headers):
    """Test getting all books."""
    response = test_client.get('/api/books', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 5
    assert 'pagination' in data

def test_get_single_book(test_client, init_database, auth_headers):
    """Test getting a single book by ID."""
    response = test_client.get('/api/books/1', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert data['data']['title'] == 'The Great Gatsby'
    assert data['data']['author'] == 'F. Scott Fitzgerald'

def test_get_nonexistent_book(test_client, init_database, auth_headers):
    """Test getting a book that doesn't exist."""
    response = test_client.get('/api/books/999', headers=auth_headers)
    
    assert response.status_code == 404

def test_create_book(test_client, init_database, auth_headers, new_book_data):
    """Test creating a new book."""
    response = test_client.post(
        '/api/books',
        data=json.dumps(new_book_data),
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert data['data']['title'] == 'Test Book'
    assert data['message'] == 'Book created successfully'

def test_create_book_invalid_data(test_client, init_database, auth_headers, invalid_book_data):
    """Test creating a book with invalid data."""
    response = test_client.post(
        '/api/books',
        data=json.dumps(invalid_book_data),
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert data['success'] == False

def test_update_book(test_client, init_database, auth_headers):
    """Test updating a book."""
    update_data = {
        'title': 'Updated Title',
        'author': 'Updated Author',
        'genre': 'Updated Genre',
        'publication_year': 2023,
        'availability': False
    }
    
    response = test_client.put(
        '/api/books/1',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert data['data']['title'] == 'Updated Title'
    assert data['data']['availability'] == False

def test_update_nonexistent_book(test_client, init_database, auth_headers):
    """Test updating a book that doesn't exist."""
    update_data = {
        'title': 'Updated Title',
        'author': 'Updated Author',
        'genre': 'Updated Genre',
        'publication_year': 2023
    }
    
    response = test_client.put(
        '/api/books/999',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    
    assert response.status_code == 404

def test_delete_book(test_client, init_database, auth_headers):
    """Test deleting a book."""
    response = test_client.delete('/api/books/1', headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verify the book was deleted
    response = test_client.get('/api/books/1', headers=auth_headers)
    assert response.status_code == 404

def test_delete_nonexistent_book(test_client, init_database, auth_headers):
    """Test deleting a book that doesn't exist."""
    response = test_client.delete('/api/books/999', headers=auth_headers)
    
    assert response.status_code == 404

def test_search_books_by_title(test_client, init_database, auth_headers):
    """Test searching books by title."""
    response = test_client.get('/api/books?q=gatsby', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'The Great Gatsby'

def test_search_books_by_author(test_client, init_database, auth_headers):
    """Test searching books by author."""
    response = test_client.get('/api/books?q=orwell', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 1
    assert data['data'][0]['author'] == 'George Orwell'

def test_search_nonexistent_book(test_client, init_database, auth_headers):
    """Test searching for a book that doesn't exist."""
    response = test_client.get('/api/books?q=nonexistentbook123', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 0

def test_filter_books_by_genre(test_client, init_database, auth_headers):
    """Test filtering books by genre."""
    response = test_client.get('/api/books?genre=Fiction', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 1
    assert data['data'][0]['genre'] == 'Fiction'

def test_filter_books_by_availability(test_client, init_database, auth_headers):
    """Test filtering books by availability."""
    response = test_client.get('/api/books?availability=false', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    # Should only get the book with availability=False
    assert all(book['availability'] == False for book in data['data'])

def test_pagination(test_client, init_database, auth_headers):
    """Test pagination functionality."""
    response = test_client.get('/api/books?page=1&per_page=2', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['data']) == 2
    assert data['pagination']['current_page'] == 1
    assert data['pagination']['per_page'] == 2
    assert data['pagination']['total'] == 5
    assert data['pagination']['pages'] == 3

def test_sort_books_by_title(test_client, init_database, auth_headers):
    """Test sorting books by title."""
    response = test_client.get('/api/books?sort_by=title&sort_order=asc', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    # Check if books are sorted by title alphabetically
    titles = [book['title'] for book in data['data']]
    assert titles == sorted(titles)

def test_invalid_page_parameter(test_client, init_database, auth_headers):
    """Test invalid page parameter."""
    response = test_client.get('/api/books?page=0&per_page=10', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    # Should default to page 1
    assert data['pagination']['current_page'] == 1