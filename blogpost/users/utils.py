import datetime
from werkzeug.security import generate_password_hash


def to_dict(req):
    return {'username': req.json['username'],
            'password': generate_password_hash(req.json['password']),
            'date_registered': datetime.datetime.utcnow()}
