from django.db import models


class Law(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField()
    canon = models.TextField(blank=True)