import os
from django.db import models
from core.models import Territory

# Create your models here.
def get_image_upload_path(instance, filename):
    """
    Generate a structured upload path and filename for images.
    
    Args:
        instance (image): The Image instance.
        filename (str): The name of the uploaded file.
        
    Returns:
        str: The constructed upload path.
    """
    
    # Extract file extension
    ext = os.path.splitext(filename)[1]
    
    territory_obj = Territory.objects.get(territory=instance.territory.territory)
    zone = territory_obj.zone_name
    region = territory_obj.region_name
    dr_folder = f"{instance.dr_id}-{instance.dr_name.replace(' ', '_')}" if instance.dr_name else instance.dr_id
    # Construct filename
    filename = f"{instance.territory.territory}_{instance.dr_id}_{instance.dr_name}{ext}"
    
    # Construct path and return
    return os.path.join('anniversary',zone, region, instance.territory.territory,dr_folder, filename)

class Anniversary(models.Model):
    """
    Model to represent a doctor's gift catalog.
    """
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='anniversary')
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, max_length=255)
    anniversary_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'dr_anniversary'
        verbose_name = "Doctor Anniversary"
        verbose_name_plural = "Doctor Anniversary"