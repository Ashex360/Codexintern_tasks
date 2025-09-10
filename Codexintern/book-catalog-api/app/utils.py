import re
from datetime import datetime
from functools import wraps
from flask import request, jsonify
from app import db

def validate_isbn(isbn):
    """
    Validate ISBN format (both ISBN-10 and ISBN-13)
    Returns: (is_valid, cleaned_isbn)
    """
    if not isbn:
        return False, None
    
    # Remove hyphens and spaces
    cleaned_isbn = re.sub(r'[-\s]', '', isbn)
    
    # Check length
    if len(cleaned_isbn) not in [10, 13]:
        return False, cleaned_isbn
    
    # Validate ISBN-10
    if len(cleaned_isbn) == 10:
        return validate_isbn10(cleaned_isbn), cleaned_isbn
    
    # Validate ISBN-13
    if len(cleaned_isbn) == 13:
        return validate_isbn13(cleaned_isbn), cleaned_isbn
    
    return False, cleaned_isbn

def validate_isbn10(isbn):
    """Validate ISBN-10 format"""
    if len(isbn) != 10:
        return False
    
    # Check if first 9 characters are digits and last character is digit or 'X'
    if not (isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X')):
        return False
    
    # Calculate checksum
    total = 0
    for i in range(9):
        total += int(isbn[i]) * (10 - i)
    
    # Handle check digit (last character)
    check_digit = 10 if isbn[-1].upper() == 'X' else int(isbn[-1])
    total += check_digit
    
    return total % 11 == 0

def validate_isbn13(isbn):
    """Validate ISBN-13 format"""
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    
    # Calculate checksum
    total = 0
    for i in range(12):
        multiplier = 1 if i % 2 == 0 else 3
        total += int(isbn[i]) * multiplier
    
    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(isbn[-1])

def format_isbn(isbn):
    """Format ISBN in standard format"""
    if not isbn:
        return None
    
    cleaned_isbn = re.sub(r'[-\s]', '', isbn)
    
    if len(cleaned_isbn) == 10:
        return f"{cleaned_isbn[0:1]}-{cleaned_isbn[1:4]}-{cleaned_isbn[4:9]}-{cleaned_isbn[9:]}"
    elif len(cleaned_isbn) == 13:
        return f"{cleaned_isbn[0:3]}-{cleaned_isbn[3:4]}-{cleaned_isbn[4:6]}-{cleaned_isbn[6:12]}-{cleaned_isbn[12:]}"
    
    return cleaned_isbn

def validate_publication_year(year):
    """Validate publication year"""
    current_year = datetime.now().year
    return 1000 <= year <= current_year

def paginate_query(query, page, per_page):
    """
    Paginate a SQLAlchemy query
    Returns: (paginated_items, total_count, total_pages)
    """
    page = max(1, page)
    per_page = max(1, min(per_page, 100))  # Limit to 100 items per page
    
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': items.items,
        'total': items.total,
        'pages': items.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': items.has_next,
        'has_prev': items.has_prev
    }

def build_pagination_links(endpoint, page, per_page, total_pages, **filters):
    """Build pagination links for API responses"""
    base_url = f"{request.host_url.rstrip('/')}{endpoint}"
    
    query_params = []
    for key, value in filters.items():
        if value is not None:
            query_params.append(f"{key}={value}")
    
    query_string = "&".join(query_params)
    if query_string:
        query_string = f"&{query_string}"
    
    links = {
        'self': f"{base_url}?page={page}&per_page={per_page}{query_string}",
        'first': f"{base_url}?page=1&per_page={per_page}{query_string}",
        'last': f"{base_url}?page={total_pages}&per_page={per_page}{query_string}" if total_pages > 0 else None
    }
    
    if page > 1:
        links['prev'] = f"{base_url}?page={page-1}&per_page={per_page}{query_string}"
    
    if page < total_pages:
        links['next'] = f"{base_url}?page={page+1}&per_page={per_page}{query_string}"
    
    return links

def handle_database_operation(func):
    """
    Decorator to handle database operations with proper error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            return {
                'error': 'Database operation failed',
                'message': str(e)
            }, 500
    return wrapper

def sanitize_input(text, max_length=None):
    """
    Sanitize user input by removing potentially harmful characters
    and limiting length if specified
    """
    if not text:
        return text
    
    # Remove HTML tags and potentially harmful characters
    sanitized = re.sub(r'<[^>]*>', '', text)  # Remove HTML tags
    sanitized = re.sub(r'[\\/*?<>|]', '', sanitized)  # Remove problematic characters
    
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def generate_book_slug(title, author):
    """
    Generate a URL-friendly slug for books
    Format: author-lastname-title-with-dashes
    """
    if not title or not author:
        return None
    
    # Extract last name from author
    author_parts = author.split()
    last_name = author_parts[-1] if author_parts else author
    
    # Create slug
    title_slug = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    title_slug = re.sub(r'\s+', '-', title_slug)
    
    author_slug = re.sub(r'[^a-zA-Z0-9]', '', last_name.lower())
    
    return f"{author_slug}-{title_slug}"

def format_response(data, status=200, message=None, pagination=None):
    """
    Standardize API response format
    """
    response = {
        'success': status in [200, 201],
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if message:
        response['message'] = message
    
    if pagination:
        response['pagination'] = pagination
    
    return jsonify(response), status

def log_operation(operation, details):
    """
    Simple logging utility for database operations
    """
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {operation}: {details}")

# Utility functions for filtering and sorting
def apply_filters(query, model, filters):
    """
    Apply filters to a SQLAlchemy query
    """
    for field, value in filters.items():
        if hasattr(model, field) and value is not None:
            if isinstance(value, list):
                query = query.filter(getattr(model, field).in_(value))
            else:
                query = query.filter(getattr(model, field) == value)
    return query

def apply_sorting(query, model, sort_by, sort_order='asc'):
    """
    Apply sorting to a SQLAlchemy query
    """
    if sort_by and hasattr(model, sort_by):
        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(model, sort_by).desc())
        else:
            query = query.order_by(getattr(model, sort_by).asc())
    return query

def parse_boolean(value):
    """
    Parse various boolean representations to Python boolean
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['true', '1', 'yes', 'y', 'on']
    if isinstance(value, int):
        return value == 1
    return bool(value)