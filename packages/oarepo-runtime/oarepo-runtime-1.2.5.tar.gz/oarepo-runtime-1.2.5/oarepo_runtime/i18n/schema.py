import langcodes
from marshmallow import Schema, fields, ValidationError, validates

"""
Marshmallow schema for multilingual strings. Consider moving this file to a library, not generating
it for each project.
"""


class MultilingualSchema(Schema):
    lang = fields.String(required=True)
    value = fields.String(required=True)

    @validates("lang")
    def validate_lang(self, value):
        if value != '_' and not langcodes.Language.get(value).is_valid():
            raise ValidationError("Invalid language code")


def MultilingualField(*args, **kwargs):
    return fields.List(fields.Nested(MultilingualSchema), *args, **kwargs)

class MultilingualUISchema(Schema):
    lang = fields.String(required=True)
    value = fields.String(required=True)

    @validates("lang")
    def validate_lang(self, value):
        if value != '_' and not langcodes.Language.get(value).is_valid():
            raise ValidationError("Invalid language code")

def MultilingualUIField(*args, **kwargs):
    return fields.List(fields.Nested(MultilingualSchema), *args, **kwargs)