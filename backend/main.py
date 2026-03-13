from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash, check_password_hash
import click
from models import db, TodoItem, Comment
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
import os
from flask import send_from_directory

# --------------------
# App setup
# --------------------
app = Flask(__name__)
CORS(app)

# Try to import local config, but fail gracefully in production
try:
    from local_config import CONFIG_DB_URI, CONFIG_JWT_SECRET
except ImportError:
    # local_config.py doesn't exist (expected in Cloud Run)
    CONFIG_DB_URI = 'sqlite:///todos.db'
    CONFIG_JWT_SECRET = 'fdslkfjsdlkufewhjroiewurewrew'
except Exception as e:
    # local_config exists but has errors
    print(f"Warning: Error loading local_config: {e}")
    CONFIG_DB_URI = 'sqlite:///todos.db'
    CONFIG_JWT_SECRET = 'fdslkfjsdlkufewhjroiewurewrew'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI','sqlite:///todos.db') 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY','fdslkfjsdlkufewhjroiewurewrew')
jwt = JWTManager(app)

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
    
    # Create default user if not exists
    if User.query.filter_by(username="admin").first() is None:
        user = User(username="admin", full_name="Administrator")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        print("Default user created: admin / admin123")

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
@jwt_required()
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


@app.cli.command("create-user")
@click.argument("username")
@click.argument("full_name")
@click.argument("password")
def create_user(username, full_name, password):

    print(username, full_name, password)

    # เช็ค user ก่อน
    user = User.query.filter_by(username=username).first()

    if user:
        click.echo("User already exists.")
        return

    # สร้าง user ใหม่
    user = User(username=username, full_name=full_name)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    click.echo(f"User {username} created successfully.")

@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401


    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)
# --------------------
# Run
# --------------------

# Catch-all route: if the requested file exists in frontend-static, serve it;
# otherwise fall back to serving the React app's index.html.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    static_dir = os.path.join(app.root_path, 'frontend-static')
    # If a specific file is requested and exists, serve it
    if path and os.path.isfile(os.path.join(static_dir, path)):
        return send_from_directory('frontend-static', path)
    # Otherwise serve the app entrypoint
    return send_from_directory('frontend-static', 'index.html')

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_ENV", "development") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

