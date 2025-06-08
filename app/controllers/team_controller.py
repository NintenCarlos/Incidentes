from flask import Blueprint, request, jsonify
from app.models.team_model import Team
from app import mongo
from bson import ObjectId

team_bp = Blueprint("teams", __name__, url_prefix="/teams")

@team_bp.route("/create", methods=["POST"])
def create_team():
    data = request.get_json()
    
    name = data.get("name")
    
    if not name: 
        jsonify({
            "error": "Faltan atributos."
        }), 400
    
    team = Team.from_dict(data)
    team.members = []
    team.status = "active"
    
    result = mongo.db.teams.insert_one(team.to_dict())
    return jsonify({
        "user": str(result.inserted_id)
    }), 200
    
@team_bp.route("/<team_id>/add-member", methods=["PATCH"])
def add_teammember(team_id): 
    data = request.get_json()
    member = data.get("member")
    
    if not member: 
        return jsonify({
            "error": "Faltan atributos."
        }), 400
        
    team = mongo.db.teams.find_one({"_id": ObjectId(team_id)})
    if not team: 
        return jsonify({
            "error": "No se encontró un equipo."
        })
    
    mongo.db.teams.update_one({"_id": ObjectId(team_id)}, {"$push": {"members": member}})
    return jsonify({"msg": f"{member} ha sido agregado."})