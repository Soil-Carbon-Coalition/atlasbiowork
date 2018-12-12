from wq.db import rest
from .models import Site, ObservationType, Observation, Map
from .serializers import ObservationTypeSerializer, ObservationSerializer, MapSerializer
from django.conf import settings

rest.router.register_model(
    Site,
    fields="__all__",
    cache="all",
    map=[{
        'mode': 'list',
	'autoLayers': True,
    }, {
        'mode': 'detail',
	'autoLayers': True,
    }, {
        'mode': 'edit',
	'autoLayers': True,
    }],
    #partial=True,
)

rest.router.register_model(
    ObservationType,
    serializer=ObservationTypeSerializer,
    fields="__all__",
)

#this could enable filtering of own observations
def user_filter(qs, request):
    if request.user.is_authenticated():
        return qs.filter(user=request.user)
    else:
        return qs.none()


rest.router.register_model(
    Observation,
    serializer=ObservationSerializer,
    fields="__all__",
    cache= "none",
    
    map=[{
        'mode': 'list',
	'autoLayers': True,
    }, {
        'mode': 'detail',
	'autoLayers': True,
    }],
)


rest.router.register_model(
    Map,
    serializer=MapSerializer,
    fields="__all__",
)



rest.router.add_page('index', {'url': ''})
rest.router.add_page('locate', {
    'url': 'locate',
    'map': {'layers': []},
    'locate': True
})

rest.router.set_extra_config(
    mapbox_token=settings.MAPBOX_TOKEN,
)
