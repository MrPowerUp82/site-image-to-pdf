from django.db import models

class Images(models.Model):
    image=models.FileField(upload_to='upload',null=True, blank=True)

# Create your models here.
