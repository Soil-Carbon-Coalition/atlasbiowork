from rest_framework import serializers
from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns.serializers import FiledModelSerializer
from html_json_forms import parse_json_form
from .models import Site
import json


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

        if data.get('site_data', None):
            self.create_site(data)

        data.setdefault('values', {})
        for key in list(data.keys()):
            if key not in set_fields:
                data['values'][key] = data.pop(key)

        return super().to_internal_value(data)

    def create_site(self, data):
        # FIXME: Use a proper Serializer class for this?
        sdata = json.loads(data['site_data'])
        geom = "POINT(%s %s)" % (
            sdata.get('longitude', 0),
            sdata.get('latitude', 0),
        )
        # FIXME: handle failure e.g. due to non-unique site id
        data['site_id'] = Site.objects.create(
            name=sdata.get('name', None),
            geometry=geom,
            accuracy=sdata.get('accuracy', None),
        ).pk
        del data['site_data']
