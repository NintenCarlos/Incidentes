from app.schema.incident_schema import IncidentSchema

class Incident (IncidentSchema): 
    def __init__(self, name, description, status, place): 
        self.name = name
        self.description = description
        self.status = status
        self.place = place
    
    def to_dict(self): 
        return {
            "name" : self.name,
            "description" : self.description,
            "status" : self.status,
            "place" : self.place
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status"),
            password=data.get("password")
        )    