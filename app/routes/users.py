from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from ..models.user import User
from .. import db

bp = Blueprint('users', __name__)

@bp.get('/me')
@jwt_required()
@swag_from({'responses': {200: {'description': 'Current user'}}})
def me():
    uid = get_jwt_identity()
    user = User.query.get_or_404(uid)
    return {'user': user.to_dict()}, 200

@bp.put('/me')
@jwt_required()
def update_me():
    uid = get_jwt_identity()
    user = User.query.get_or_404(uid)
    data = request.get_json() or {}
    if 'name' in data:
        user.name = data['name']
    db.session.commit()
    return {'user': user.to_dict()}, 200
