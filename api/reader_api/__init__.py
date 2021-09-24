from flask import Flask

from reader_api.init_database import init_db
import reader_api.auth as auth
import reader_api.sections as sections
import reader_api.articles as articles
import reader_api.comments as comments


def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"

    app.cli.add_command(init_db)
    app.register_blueprint(auth.bp)
    app.register_blueprint(sections.bp)
    app.register_blueprint(articles.bp)
    app.register_blueprint(comments.bp)

    return app
