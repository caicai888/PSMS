#! /usr/bin/env python
# coding=utf-8
from functools import wraps
import json
from flask import session
from main import db
from main.models import User, Permissions, UserPermissions


class Permission(object):
    @classmethod
    def check(cls, *args, **kwargs):
        def decoratored(func):
            def wrap(*args, **kw):
                models = kwargs.get('models')
                if 'user_id' in session:
                    user_id = session['user_id']
                    curent_user = db.session.query(User).filter_by(id=user_id).first()

                    if not curent_user:
                        return json.dumps(dict(code=403, message='not have this user'))
                    else:
                        permission_list = []
                        user_permissions = db.session.query(UserPermissions).filter_by(user_id=user_id).first()
                        for user_permission in user_permissions.permissions_id.split(','):
                            permission_list.append(
                                db.session.query(Permissions).filter_by(id=int(user_permission)).first().name)
                        for model in models:
                            if model not in permission_list:
                                return json.dumps(dict(code=403, message='no permission'))
                else:
                    return json.dumps(dict(code=403, message='user not login'))
                return func(*args, **kw)

            return wrap

        return decoratored
