from marshmallow import Schema, fields, validate, INCLUDE


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate.Email(error="Not a valid email address"))
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    role_id = fields.Str(required=True)  # validate from DB, also check length
    track_id = fields.Str()  # validate from DB, also check length
    _id = fields.Str(dump_only=True)
    # tentative
    role = fields.Dict(dump_only=True)
    track = fields.Dict(dump_only=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
