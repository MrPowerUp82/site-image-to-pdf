from django.db import models
from uuid import uuid4

class Images(models.Model):
    image=models.ImageField(upload_to='upload',null=True, blank=True)
    uuid=models.CharField(max_length=255,default=uuid4)

# Create your models here.
