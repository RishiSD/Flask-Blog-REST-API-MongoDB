import datetime


def to_dict(req):
    return {'username': req.json['username'],
            'password': req.json['password'],
            'date_registered': datetime.datetime.utcnow()}
