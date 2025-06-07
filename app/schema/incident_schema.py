from marshmallow import Schema, fields

class IncidentSchema(Schema): 
    name = fields.Str(
        required= True,
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "No debde de estar vacío"}
    )
    
    description = fields.Str(
        required= True,
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "No debde de estar vacío"}
    )
    
    status = fields.Str(
        required=True, 
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "No debde de estar vacío"}
        
    )
    
    place = fields.Str(
        required=True, 
        validate= lambda x: len(x) > 0,
        error_messages= {"error": "No debde de estar vacío"}
        
    )
    