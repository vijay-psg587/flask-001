from marshmallow import Schema, fields


class TrackSchema(Schema):
    _id = fields.Str(dump_only=True)
    track_name = fields.Str()
    start_date = fields.Str()
    end_date = fields.Str()
    language = fields.Str()
    created_by = fields.Str(load_only=True)
    updated_by = fields.Str(load_only=True)
    updated_at = fields.Str(load_only=True)
    created_at = fields.Str(load_only=True)
    status = fields.Str()
    track_lead = fields.Str()
