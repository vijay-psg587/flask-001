from marshmallow import Schema, fields


class PiaDataResponseSchema(Schema):
    track_name = fields.Str(required=True)
    track_id = fields.Field(required=True)
    usr_ctx = fields.Field(required=True)
    report_date = fields.Str(required=True)
    pia_report = fields.Dict(required=False)
    created_by = fields.Str(required=False, load_only=True)
    updated_by = fields.Str(required=False, load_only=True)
    created_at = fields.Float(required=False, load_only=True)
    updated_at = fields.Float(required=False, load_only=True)
