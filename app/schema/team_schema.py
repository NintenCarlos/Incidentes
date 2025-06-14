from marshmallow import Schema, fields

class TeamSchema(Schema): 
    name = fields.Str(
        required= True,
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "El campo no puede estar vació."}
    )
    
    members = fields.List(
        fields.Str(),
        required=True
    )
    
    status = fields.Str(
        required=True,
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "El campo no puede estar vacío"}
    )
    
    