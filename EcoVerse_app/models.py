from django.db import models

# Create your models here.
from django.db import models

class EcoToken(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    token_mint = models.CharField(max_length=100, blank=True, null=True)
    metadata_url = models.URLField(blank=True, null=True)
    bags_url = models.URLField(blank=True, null=True)
    launch_signature = models.CharField(max_length=200, blank=True, null=True)
    is_launched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)