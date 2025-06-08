from flask import Blueprint, request, jsonify
from app.models.incident_model import Incident
from flask_jwt_extended import get_jwt_identity, jwt_required
from bson import ObjectId
from app import mongo

incident_bp = Blueprint("incidents", __name__, url_prefix="/incidents")

@incident_bp.route("/create", methods=["POST"])
def create_incident(): 
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")
    place = data.get("place")
    
    if not name or not description or not place: 
        return jsonify({
            "error" : "Faltan atributos."
        }), 400
        
    new_incident = Incident.from_dict(data)
    new_incident.status = "pending"
    
    incident = mongo.db.incidents.insert_one(new_incident.to_dict())
    
    return jsonify({
        "incident": str(incident.inserted_id)
    }),200
    
@incident_bp.route("/search/status/", methods=["GET"])
def seach_incidents_by_status(): 
    status = request.args.get("status") 
    
    data = mongo.db.incidents.find({"status": status})
    
    result = []
    
    for datum in data: 
        datum["_id"] = str(datum["_id"])
        result.append(datum)
    
    return jsonify(result), 200

@incident_bp.route("/search/place/", methods=["GET"])
def search_incidents_by_place(): 
    place = request.args.get("place")
    
    data = mongo.db.incidents.find({
        "status": "pending",
        "place": place
    })
    
    result = []
    
    for datum in data: 
        datum["_id"] = str(datum["_id"])
        result.append(datum)
    
    return jsonify(result), 200

@incident_bp.route("/update/status/<incident_id>", methods=["PATCH"])
def update_incident_status(incident_id): 
    incident = mongo.db.incidents.find_one({
        "_id": ObjectId(incident_id)
    })
    
    if not incident: 
        return jsonify({
            "error" : "No se encontró un incidente válido."
        }), 400
    
    status = incident["status"] 
    
    if status == "pending": 
        mongo.db.incidents.update_one({
            "_id": ObjectId(incident_id)},
            {"$set": {"status": "complete"}}
        )
        
        return jsonify({
            "msg": "El estado se ha actualizado con éxito."
        }), 200
        
    if status == "complete": 
        mongo.db.incidents.update_one({
            "_id": ObjectId(incident_id)},
            {"$set": {"status": "pending"}
        })
        
        return jsonify({
            "msg": "El estado se ha actualizado con éxito."
        }), 200

@incident_bp.route("/update/<incident_id>", methods=["PUT"])
def update_incident(incident_id): 
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")
    place = data.get("place")
    
    if not name or not description or not place: 
        return jsonify({
            'error': 'Faltan atributos.'
        }), 400
        
    incident = mongo.db.incidents.find_one({
        "_id": ObjectId(incident_id)
    })
    
    if not incident: 
        return jsonify({
            "error" : "No se encontró un incidente válido."
        }), 400
        
    mongo.db.incidents.update_one({
            "_id": ObjectId(incident_id)},
            {"$set": {"name": name,
                      "description": description,
                      "status": incident["status"],
                      "place": place
                      }})
    
    updated_incident = mongo.db.incidents.find_one({
        "_id": ObjectId(incident_id)
    })
    
    return jsonify({
        "msg": updated_incident
    }), 200
    
@incident_bp.route("/delete/<inserted_id>", methods=["DELETE"])
def delete_incident(inserted_id): 
    
    incident = mongo.db.incidents.find_one({
        "_id": ObjectId(inserted_id)
    })
    
    if not incident: 
        return jsonify({
            "error": "No se encontró el incidente."
        })
        
    if incident["status"] == "pending": 
        return jsonify({
            "error": "No se puede borrar un incidente sino está resuelto."
        }), 400
        
    mongo.db.incidents.delete_one({
        "_id": ObjectId(inserted_id)
    })
    
    return jsonify({
        "msg": "El incidente se ha eliminado."
    })