from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from blogpost.config import Config

mongo = PyMongo()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

    from blogpost.utils import (
        check_if_token_in_blacklist,
        expired_token_callback,
        invalid_token_callback,
        missing_token_callback,
        token_not_fresh_callback,
        revoked_token_callback
    )

    from blogpost.posts.routes import posts
    from blogpost.users.routes import users
    app.register_blueprint(posts)
    app.register_blueprint(users)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
