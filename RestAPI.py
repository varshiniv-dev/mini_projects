# write a python program on rest API using flask/flask API- user authentication, crud operation, json response, error handling, notes api, blog api, student api
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import timedelta
from functools import wraps
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# User Model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
# Student Model


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Float, nullable=False)


# Create the database
with app.app_context():
    db.create_all()
# Admin required decorator


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, description="Admin access required")
        return fn(*args, **kwargs)
    return wrapper
# User Registration


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, is_admin=data.get(
        'is_admin', False))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201
# User Login


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(
            identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401
# CRUD Operations for Students


@app.route('/students', methods=['POST'])
@admin_required
def add_student():
    data = request.get_json()
    new_student = Student(name=data['name'], marks=data['marks'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify(message="Student added successfully"), 201


@app.route('/students/<int:id>', methods=['PUT'])
@admin_required
def update_student(id):
    data = request.get_json()
    student = Student.query.get_or_404(id)
    student.name = data['name']
    student.marks = data['marks']
    db.session.commit()
    return jsonify(message="Student updated successfully"), 200


@app.route('/students/<int:id>', methods=['DELETE'])
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify(message="Student deleted successfully"), 200


@app.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(id=student.id, name=student.name, marks=student.marks), 200


@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    result = [{"id": s.id, "name": s.name, "marks": s.marks} for s in students]
    return jsonify(students=result), 200
# Error Handlers


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="An internal error occurred"), 500


if __name__ == '__main__':
    app.run(debug=True)
    base_dir = r"C:\Users\Asus\OneDrive\Documents\GitHub\test_folder"   # CHANGE THIS
    fas.schedule_cleanup(60)
    # fas.schedule_cleanup(60)
    fas.generate_report()
    fas.delete_duplicates()
    fas.rename_files()
    fas.organize_files()
    fas = FileAutomationSystem(base_dir)
