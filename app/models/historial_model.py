from app.schema.historial_schema import HistorialSchema
from bson import ObjectId

class Historial(HistorialSchema): 
    def __init__(self, incident, date): 
        self.incident = incident
        self.date = date
    
    def to_dict(self): 
        return {
            "incident": ObjectId(self.incident),
            "date": self.date
        }
        
    @classmethod
    def from_dict(cls, data): 
        return cls (
            incident=data.get("incident"),
            date=data.get("date")
        )