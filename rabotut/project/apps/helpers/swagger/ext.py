from collections import OrderedDict


class ReadOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for field_name, field in super().get_fields().items():
            if not field.write_only:
                new_fields[field_name] = field
        return new_fields


class WriteOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for field_name, field in super().get_fields().items():
            if not field.read_only:
                new_fields[field_name] = field
        return new_fields


class BlankMeta:
    pass
