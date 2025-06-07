from marshmallow import Schema, fields

class HistorialSchema(Schema): 
    incident = fields.Str(
        required=True
    )
    
    date = fields.Date(
        required=True
    )