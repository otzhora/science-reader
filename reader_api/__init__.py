import os

from flask import Flask

import reader_api.auth as auth
import reader_api.sections as sections
import reader_api.articles as articles
import reader_api.comments as comments


def create_app():
    config_name = os.environ["FLASK_CONFIG"]
    app = Flask(__name__)
    app.secret_key = "dev"

    config_module = f"reader_api.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    app.register_blueprint(auth.bp)
    app.register_blueprint(sections.bp)
    app.register_blueprint(articles.bp)
    app.register_blueprint(comments.bp)

    return app
