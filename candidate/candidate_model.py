from marshmallow import Schema, fields


class CandidateResponseSchema(Schema):
    name = fields.Str(required=False)
    email = fields.Str(required=False)
    status = fields.Str(required=False)
    tracks = fields.List(fields.Str(), required=False)
    track_repos = fields.Dict(required=False)
    created_by = fields.Str(required=False, load_only=True)
    updated_by = fields.Str(required=False, load_only=True)
    created_at = fields.Str(required=False, load_only=True)
    updated_at = fields.Str(required=False, load_only=True)
