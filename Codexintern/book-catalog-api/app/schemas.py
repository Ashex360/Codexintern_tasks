from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    genre = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    publication_year = fields.Int(
        required=True, 
        validate=validate.Range(min=1000, max=2023)
    )
    availability = fields.Bool(missing=True)