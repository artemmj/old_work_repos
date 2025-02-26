import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):  # noqa: WPS110
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
