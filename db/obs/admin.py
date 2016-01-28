from django.contrib import admin
from .models import Site, Observation, ObservationType

admin.site.register(Site)
admin.site.register(Observation)
admin.site.register(ObservationType)
