from django.db.models import Model
from django.db import models
class WorkPiece(Model):
    name = models.CharField(max_length=128)
