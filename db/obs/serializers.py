from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from wq.db.rest.serializers import ModelSerializer, GeometryField
from html_json_forms import parse_json_form
from .models import Site, Observation
import json


class CurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self):
        user = super().__call__()
        return user.pk


class ObservationTypeSerializer(ModelSerializer):
    author_id = serializers.HiddenField(
        default=CurrentUserDefault()
    )
    icon = serializers.ImageField(
        required=False,
    )
class ChildObservationSerializer(ModelSerializer):
    class Meta:
        model = Observation
        fields = "__all__"
    
class ObservationSerializer(ModelSerializer):
    childobs = ChildObservationSerializer(many=True, read_only=True)  #try also adding (Required=False) to args?
    observer_id = serializers.HiddenField(
        default=CurrentUserDefault()
    )
    geometry = GeometryField(
        source="site.geometry",
        read_only=True,
    )

    def to_representation(self, obj):
        """
        Merge 'values' JSON with relational fields
        """
        data = super().to_representation(obj)
        values = data.pop('values') or {}
        for key, val in values.items():
            if isinstance(val, list):
                for i, v in enumerate(val):
                    if isinstance(v, dict):
                        v['@index'] = i
        data.update(values)
        return data

    def to_internal_value(self, data):
        """
        Extract 'values' JSON from relational and built-in form fields
        """

        # Save files and return paths
        for key, value in data.items():
             if isinstance(value, UploadedFile):
                 path = 'observations/' + value.name
                 data[key] = default_storage.save(path, value)

        # Convert nested keys to JSON structure
        data = parse_json_form(data)
        fixed_fields = list(self.get_fields().keys()) + [
            'csrfmiddlewaretoken', '_method',
        ]

        # On-the-fly site creation (New Site + Observation)
        if data.get('site_data', None):
            self.create_site(data)

        # Extract JSON data into 'values' field, leaving relational and
        # built-in fields in place.
        data.setdefault('values', {})
        for key in list(data.keys()):
            if key not in fixed_fields:
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

class MapSerializer(ModelSerializer):
    author_id = serializers.HiddenField(
        default=CurrentUserDefault()
    )
    
    def to_representation(self, obj):
        """
        Merge 'values' JSON with relational fields
        """
        data = super().to_representation(obj)
        values = data.pop('values') or {}
        for key, val in values.items():
            if isinstance(val, list):
                for i, v in enumerate(val):
                    if isinstance(v, dict):
                        v['@index'] = i
        data.update(values)
        return data
