from django.db import models
from core.models import Territory

# Create your models here.
class GreenCorner(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    dr_address = models.CharField(max_length=200, blank=True, null=True)
    rm_phone = models.CharField(max_length=20, blank=True, null=True)
    first_flower_plant = models.CharField(max_length=30, blank=True, null=True)
    second_flower_plant = models.CharField(max_length=30, blank=True, null=True)
    third_flower_plant = models.CharField(max_length=30, blank=True, null=True)
    first_medicine_plant = models.CharField(max_length=30, blank=True, null=True)
    second_medicine_plant = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)