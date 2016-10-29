from django.contrib import admin
from django.contrib.gis import admin
from .models import Site, Observation, ObservationType, Map

class SiteAdmin(admin.GeoModelAdmin):
    openlayers_url = "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js"

admin.site.register(Site, SiteAdmin)
admin.site.register(Observation)
admin.site.register(ObservationType)
admin.site.register(Map)