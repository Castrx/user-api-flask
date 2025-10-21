from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flasgger.utils import swag_from
from .. import db
from ..models.user import User

bp = Blueprint('auth', __name__)

@bp.post('/register')
@swag_from({'responses': {201: {'description': 'User created'}}})
def register():
    data = request.get_json() or {}
    if not all(k in data for k in ('email', 'name', 'password')):
        return {'message': 'Missing fields'}, 400
    if User.query.filter_by(email=data['email']).first():
        return {'message': 'Email already exists'}, 409
    user = User(email=data['email'], name=data['name'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return {'user': user.to_dict()}, 201

@bp.post('/login')
@swag_from({'responses': {200: {'description': 'Token issued'}}})
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password', '')):
        return {'message': 'Invalid credentials'}, 401
    token = create_access_token(identity=user.id)
    return {'access_token': token}, 200
