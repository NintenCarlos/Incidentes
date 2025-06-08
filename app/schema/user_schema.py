from marshmallow import Schema, fields

class UserSchema (Schema): 
    name = fields.Str(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages= { "error": "El nombre es requerido."}
    )
    
    email = fields.Str(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={"error": "El correo es requerido."}
    )
    
    password = fields.Str(
        required=True,
        validate=lambda x: len(x) > 4,
        error_messages= {"error": "La contraseña necesita mínimo 5 carácteres."}
    )
    
    status = fields.Str(
        required=True,
        validate= lambda x: len(x) > 0,
        error_messages={"error": "El estado es requerido."}
    )