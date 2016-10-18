from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
import xlsconv

XLSCONV_TEMPLATE = settings.BASE_DIR + '/xlsconv_templates/%s.html'


class Site(models.Model):
    name = models.CharField(max_length=100, unique=False)
    geometry = models.GeometryField(srid=settings.SRID)
    accuracy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='forms')
    description = models.TextField()
    author = models.ForeignKey('auth.User')
    xlsform = models.FileField(upload_to='forms', null=True, blank=True)
    form_json = JSONField(null=True, blank=True)
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

    def __str__(self):
        return "%s posted %s" % (
            self.type, self.entered.date()
        )
    class Meta:
        ordering = ['-entered']    

        
