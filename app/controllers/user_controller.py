from flask import Blueprint, request, jsonify
from app.models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson import ObjectId
from app import mongo

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/create", methods=["POST"])
def create_user(): 
    data = request.get_json() 
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not name or not email or not password: 
        return jsonify({
            "error" : "Faltan atributos"
        }), 400

    user = User.from_dict(data)
    user.password = generate_password_hash(user.password)
    user.status = "active"
    result = mongo.db.users.insert_one(user.to_dict())

    return jsonify({
        "user": str(result.inserted_id)
    }), 200
    
@user_bp.route("/login", methods=["POST"])
def login_user(): 
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password: 
        return jsonify({
            "error" : "Faltan atributos"
        }), 400
        
    user = mongo.db.users.find_one({"email": email})
    
    if not user: 
        return jsonify({
            "error": "No se encontró a ningun usuario con ese correo"
        }), 400
        
    if not check_password_hash(user["password"], password): 
       return jsonify({
            "error": "Las contraseñas son diferentes."
        }), 400
    
    access_token = create_access_token(identity=str(user["_id"]))
    
    return jsonify({
        "access_token": access_token
    })
    
@user_bp.route("/update/status/<user_id>", methods=["PATCH"])
def update_user_status(user_id): 
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user: 
        return jsonify({
            "error": "No se encontró un usuario"
        })
        
    if user["status"] == "active": 
        mongo.db.users.update_one({
            "_id": ObjectId(user_id)},
            {"$set": {"status": "inactive"}}
        )
        
        return jsonify({"msg": "El estado se ha actualizado"}), 200
    
    if user["status"] == "inactive": 
        mongo.db.users.update_one({
            "_id": ObjectId(user_id)},
            {"$set": {"status": "active"}}
        )
        
        return jsonify({"msg": "El estado se ha actualizado"}), 200


    
@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user(): 
    user_id = get_jwt_identity()
    
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if user["status"] == "active": 
        return jsonify({
            "error": "No se puede eliminar a un usuario activo."
        })
    
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    
    return jsonify({
        "msg" : "Usuario eliminado."
    }), 200
    
