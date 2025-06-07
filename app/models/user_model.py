from app.schema.user_schema import UserSchema

class User(UserSchema): 
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        
    def to_dict(self): 
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )        