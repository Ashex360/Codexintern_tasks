from flask import Blueprint, request, jsonify
from app import db
from app.models import Book
from app.schemas import BookSchema
from sqlalchemy import or_

bp = Blueprint('api', __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@bp.route('/books', methods=['GET'])
def get_books():
    # Search functionality
    search_query = request.args.get('q')
    if search_query:
        books = Book.query.filter(
            or_(
                Book.title.ilike(f'%{search_query}%'),
                Book.author.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        books = Book.query.all()
    
    return jsonify(books_schema.dump(books))

@bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book_schema.dump(book))

@bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        publication_year=data['publication_year'],
        availability=data.get('availability', True)
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify(book_schema.dump(book)), 201

@bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book.title = data['title']
    book.author = data['author']
    book.genre = data['genre']
    book.publication_year = data['publication_year']
    book.availability = data.get('availability', book.availability)
    
    db.session.commit()
    
    return jsonify(book_schema.dump(book))

@bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    
    return '', 204