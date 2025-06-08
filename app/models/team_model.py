from app.schema.team_schema import TeamSchema

class Team(TeamSchema): 
    def __init__(self, name, members, status): 
        self.name = name
        self.members = members
        self.status = status
        
    def to_dict(self): 
        return {
            "name": self.name,   
            "members": self.members,   
            "status": self.status,      
        }
        
    @classmethod
    def from_dict(cls, data): 
        return cls(
            name=data.get("name"),
            members=data.get("members"),
            status=data.get("status"),
        )   
    