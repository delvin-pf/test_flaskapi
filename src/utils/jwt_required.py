from functools import wraps
from flask import request, current_app
import jwt


def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Token de autenticação não fornecido'}, 401

        try:
           jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token inválido'}, 401

        # Se tudo estiver correto, chame a função de rota original
        return func(*args, **kwargs)

    return decorated