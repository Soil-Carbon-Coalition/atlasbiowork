from rest_framework import serializers
from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns.serializers import FiledModelSerializer
from wq.db.rest.compat import parse_json_form


class CurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self):
        user = super().__call__()
        return user.pk


class ObservationTypeSerializer(ModelSerializer):
    author_id = serializers.HiddenField(
        default=CurrentUserDefault()
    )


class ObservationSerializer(FiledModelSerializer):
    observer_id = serializers.HiddenField(
        default=CurrentUserDefault()
    )

    def to_representation(self, obj):
        """
        Merge 'values' JSON with relational fields
        """
        data = super().to_representation(obj)
        data.update(data.pop('values') or {})
        return data

    def to_internal_value(self, data):
        """
        Extract 'values' JSON from relational and built-in form fields
        """
        data = parse_json_form(data)
        set_fields = list(self.get_fields().keys()) + [
            'csrfmiddlewaretoken', '_method',
        ]
        data.setdefault('values', {})
        for key in list(data.keys()):
            if key not in set_fields:
                data['values'][key] = data.pop(key)
        return super().to_internal_value(data)
