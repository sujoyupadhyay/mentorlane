from flask import Flask, jsonify, render_template
from flasgger import Swagger

from .database import mysql_session
from .teaching_modes import teaching_mode_bp


def create_app() -> Flask:
    app = Flask(__name__)
    Swagger(app)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.route("/api/hello")
    def hello() -> tuple[dict[str, str], int]:
        """Example endpoint returning a greeting."""
        return {"message": "Hello, world!"}, 200

    app.register_blueprint(teaching_mode_bp)

    return app
