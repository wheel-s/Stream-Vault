from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.schemas.userSchema import UserSchema
from app.utils.limiter import limiter

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/users')



userschema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    error = userschema.validate(data)
    if error:
        return jsonify({"error":error}), 400

    if User.query.filter_by(username = data['username']).first():
        return jsonify({"error":"Username exists"}), 400

    user = User(username = data['username'],email=data['email'], role = data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()


    return jsonify({"message":"User created !!"}), 201


@limiter.limit("5 per minute")
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username = data['username']).first()

    if not user or not check_password_hash(user.password_hash,data['password']):
        return jsonify({"error":"please provide valid credentials"}), 401
    
    token = create_access_token(identity= {"id": user.id, "role": user.role})
    return jsonify({"token": token}), 200

