from flask import Flask
from flask_cors import CORS
from app.api import grades

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(grades.bp)
    
    return app
