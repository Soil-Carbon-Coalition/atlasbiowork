from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
import xlsconv

XLSCONV_TEMPLATE = settings.BASE_DIR + '/xlsconv_templates/%s.html'


class Site(models.Model):
    name = models.CharField(max_length=100, unique=False)
    geometry = models.GeometryField(srid=settings.SRID)
    accuracy = models.FloatField(null=True, blank=True)

    wq_label_template = "{{name}}"

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-pk']
     
class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='forms')
    description = models.TextField()
    author = models.ForeignKey('auth.User')
    xlsform = models.FileField(upload_to='forms', null=True, blank=True)
    form_json = JSONField(null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    edit_html = models.TextField(null=True, blank=True)
    detail_html = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.xlsform:
            try:
                self.form_json = xlsconv.parse_xls(self.xlsform)
            except Exception as e:
                self.edit_html = "Error parsing form: %s" % e
                self.detail_html = "Error parsing form: %s" % e
            else:
                if not self.edit_html:
                    self.edit_html = self.generate_html('edit')
                if not self.detail_html:
                    self.detail_html = self.generate_html('detail')
        super().save(*args, **kwargs)

    def generate_html(self, template):
        try:
            html = xlsconv.render(
                xlsconv.html_context(self.form_json),
                XLSCONV_TEMPLATE % template,
            )
        except Exception as e:
            html = "Error generating HTML: %s" % e
        return html

    def __str__(self):
        return self.name


class Observation(models.Model):
    observer = models.ForeignKey('auth.User')
    parentobs = models.ForeignKey('self', null=True, blank=True, related_name='childobs')
    type = models.ForeignKey(ObservationType)
    entered = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site)
    values = JSONField(null=True, blank=True)

    wq_label_template = "Observation{{#date}} on {{{date}}}{{/date}}"

    def __str__(self):
        if self.type_id is None:
            return "New Observation"
        return "%s: %s" % (
            self.id, self.type
        )
    def get_ancestors(self): #this is a recursive function!!!!
        if self.parentobs is None:
            return Observation.objects.none()
        return Observation.objects.filter(pk=self.parentobs.pk) | self.parentobs.get_ancestors()

    class Meta:
        ordering = ['-entered']    

        
class Map(models.Model):
    author = models.ForeignKey('auth.User')
    entered = models.DateTimeField(auto_now_add=True)
    name = name = models.CharField(max_length=100, unique=False)
    values = JSONField(null=True, blank=True)

    def __str__(self):
        return "Map created on %s" % (
            self.entered.date()
        )

    class Meta:
        ordering = ['-pk']    
