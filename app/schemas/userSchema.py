from marshmallow import  fields, Schema, validate


class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True,validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password =fields.Str(required=True,load_only=True, validate = validate.Length(min=4))
    role = fields.Str(load_only=True, validate=validate.OneOf(["guest", "admin"]))