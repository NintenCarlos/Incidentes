import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

# Instanciar 
load_dotenv()
jwt = JWTManager()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") 
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    
    mongo.init_app(app)
    jwt.init_app(app)
    
    from app.controllers.user_controller import user_bp
    from app.controllers.incident_controller import incident_bp
    from app.controllers.team_controller import team_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(team_bp)
    
    CORS(app)    
    
    
    return app
    
