from flask import Blueprint, request, jsonify
from models import db, Todo, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

routes = Blueprint("routes", __name__)

# ---------- AUTH ----------
@routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username=data["username"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# ---------- TODO ----------
@routes.route("/todos", methods=["POST"])
@jwt_required()
def create_todo():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_todo = Todo(title=data["title"], description=data.get("description", ""), user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Todo created successfully"}), 201

@routes.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "done": t.done} for t in todos])

@routes.route("/todos/<int:id>", methods=["PUT"])
@jwt_required()
def update_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    db.session.commit()
    return jsonify({"message": "Todo updated successfully"})

@routes.route("/todos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"})

@routes.route("/todos/<int:id>/mark-done", methods=["PATCH"])
@jwt_required()
def mark_done(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()
    todo.done = True
    db.session.commit()
    return jsonify({"message": "Todo marked as done"})
