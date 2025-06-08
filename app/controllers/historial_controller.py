from flask import jsonify, Blueprint, request
from app.models.historial_model import Historial
from bson import ObjectId
from app import mongo
from datetime import datetime

historial_bp = Blueprint("historial", __name__, url_prefix="/historial")

@historial_bp.route("/create", methods=["POST"])
def create_document(): 
    data = request.get_json()
    incident_id = data.get("incident") 
    
    if not incident_id: 
        return jsonify({"error": "Faltan atributos"}), 400
    
    incident = mongo.db.incidents.find_one({"_id": ObjectId(incident_id)})
    if not incident: 
        return jsonify({"error": "No se ha encontrado un incidente válido."}), 400
    
    historial = Historial.from_dict(data)
    historial.date = datetime.now()
    result = mongo.db.historials.insert_one(historial.to_dict())
    
    return jsonify({"historial": str(result.inserted_id)}), 200