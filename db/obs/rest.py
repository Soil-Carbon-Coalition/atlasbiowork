from wq.db import rest
from .models import Site, ObservationType, Observation, Map
from .serializers import ObservationTypeSerializer, ObservationSerializer, MapSerializer
from django.conf import settings

rest.router.register_model(
    Site,
    map={
        'list': {'autoLayers': True},
        'edit': {'autoLayers': True},
        'detail': {'autoLayers': True},
    },
    partial=True,
)

rest.router.register_model(
    ObservationType,
    serializer=ObservationTypeSerializer
)

rest.router.register_model(
    Observation,
    serializer=ObservationSerializer,
    map={
        'list': {'autoLayers': True},
        'detail': {'autoLayers': True},
    },
)


rest.router.register_model(
    Map,
    serializer=MapSerializer
)



rest.router.add_page('index', {'url': ''})
rest.router.add_page('locate', {
    'url': 'locate',
    'map': {},
    'locate': True
})

rest.router.set_extra_config(
    mapbox_token=settings.MAPBOX_TOKEN,
)
