from django.db import models


class Url(models.Model):
    link = models.URLField(max_length=2048)
    status = models.IntegerField()
    response_time = models.DecimalField(decimal_places=2, max_digits=5)
    regexp = models.CharField(max_length=1024, blank=True, null=True)
    regexp_match = models.CharField(max_length=5, blank=True, null=True)
    match_details = models.CharField(max_length=1024, blank=True, null=True)
