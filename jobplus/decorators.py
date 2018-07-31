from flask import abort
from flask_login import current_user
from functools import wraps
from jobplus.models import User


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role !=role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator

person_required = role_required(User.ROLE_USER)
company_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)

