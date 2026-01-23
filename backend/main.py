from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, TodoItem, Comment

# --------------------
# App setup
# --------------------
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# --------------------
# Initial data
# --------------------
with app.app_context():
    db.create_all()
    if TodoItem.query.count() == 0:
        db.session.add_all([
            TodoItem(title="Learn Flask"),
            TodoItem(title="Build a Flask App")
        ])
        db.session.commit()

# --------------------
# Helpers
# --------------------
def new_todo(data):
    return TodoItem(
        title=data["title"],
        done=data.get("done", False)
    )

# --------------------
# Routes
# --------------------
@app.route("/api/todos/", methods=["GET"])
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([t.to_dict() for t in todos])


@app.route("/api/todos/", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    todo = new_todo(data)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


@app.route("/api/todos/<int:id>/toggle/", methods=["PATCH"])
def toggle_todo(id):
    todo = TodoItem.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())


@app.route("/api/todos/<int:id>/", methods=["DELETE"])
def delete_todo(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"})


@app.route("/api/todos/<int:todo_id>/comments/", methods=["POST"])
def add_comment(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "message is required"}), 400

    comment = Comment(
        message=data["message"],
        todo=todo
    )

    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201


# --------------------
# Run
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
