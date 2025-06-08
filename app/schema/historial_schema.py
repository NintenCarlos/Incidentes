from marshmallow import Schema, fields, ValidationError

def validate_object_id(value): 
    from bson import ObjectId
    
    if not ObjectId.is_valid(value): 
        raise ValidationError("El valor proporcionado no es un Object_Id")
class HistorialSchema(Schema): 
    incident = fields.Str(
        required=True,
        validate=validate_object_id
    )
    
    date = fields.Date(
        required=True
    )