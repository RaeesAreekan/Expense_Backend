import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.expense_routes import expense_blueprint
from database.database import db

# Load environment variables from a .env file at the project root
load_dotenv()


def create_app():

    app = Flask(__name__)
    CORS(app, origins=["https://expenseappfrontend.web.app", "http://localhost:3000"])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Initialization ---
    db.init_app(app)
    app.register_blueprint(expense_blueprint)
    return app
