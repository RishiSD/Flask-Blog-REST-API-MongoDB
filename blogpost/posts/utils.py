import datetime


def to_dict(req):
    return {'title': req.json['title'],
            'subtitle': req.json['subtitle'],
            'author': req.json['author'],
            'content': req.json['content'],
            'date_posted': datetime.datetime.utcnow()}


def id_to_str(post):
    post['_id'] = str(post['_id'])
    return post
