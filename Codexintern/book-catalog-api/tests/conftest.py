import pytest
from app import create_app, db
from app.models import Book
from config import TestingConfig

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    # Create app with testing config
    app = create_app(TestingConfig)
    
    # Create test context
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_database(test_app):
    """Create a fresh database for each test module."""
    # Create all tables
    db.create_all()
    
    yield db
    
    # Drop all tables after tests
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def test_client(test_app):
    """Create a test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_database):
    """Initialize the database with test data."""
    # Add test books
    books = [
        Book(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            genre='Classic',
            publication_year=1925,
            availability=True
        ),
        Book(
            title='To Kill a Mockingbird',
            author='Harper Lee',
            genre='Fiction',
            publication_year=1960,
            availability=True
        ),
        Book(
            title='1984',
            author='George Orwell',
            genre='Dystopian',
            publication_year=1949,
            availability=False
        ),
        Book(
            title='Pride and Prejudice',
            author='Jane Austen',
            genre='Romance',
            publication_year=1813,
            availability=True
        ),
        Book(
            title='The Hobbit',
            author='J.R.R. Tolkien',
            genre='Fantasy',
            publication_year=1937,
            availability=True
        )
    ]
    
    for book in books:
        test_database.session.add(book)
    
    test_database.session.commit()
    
    yield test_database
    
    # Clean up after each test
    test_database.session.rollback()
    # Don't drop tables here, let test_database fixture handle it

@pytest.fixture(scope='function')
def auth_headers():
    """Fixture for authentication headers (if needed in the future)."""
    # Placeholder for when authentication is implemented
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

@pytest.fixture
def new_book_data():
    """Fixture for new book test data."""
    return {
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Test Genre',
        'publication_year': 2023,
        'availability': True
    }

@pytest.fixture
def invalid_book_data():
    """Fixture for invalid book test data."""
    return {
        'title': '',  # Empty title
        'author': '',  # Empty author
        'genre': '',  # Empty genre
        'publication_year': 1800,  # Invalid year
        'availability': 'not-a-boolean'  # Invalid boolean
    }

@pytest.fixture
def sample_search_queries():
    """Fixture for search test queries."""
    return {
        'title_search': 'gatsby',
        'author_search': 'fitzgerald',
        'genre_search': 'classic',
        'non_existent': 'nonexistentbook123'
    }