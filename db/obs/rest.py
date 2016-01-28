from wq.db import rest
from .models import Site, ObservationType, Observation
from .serializers import ObservationTypeSerializer, ObservationSerializer


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
    serializer=ObservationSerializer
)

rest.router.add_page('index', {'url': ''})
rest.router.add_page('locate', {
    'url': 'locate',
    'map': {},
    'locate': True
})
