import os
from django.db import models
from core.models import Territory

# Create your models here.
def get_image_upload_path(instance, filename):
    """
    Generate a structured upload path and filename for images.
    
    Args:
        instance (ConferenceImage): The ConferenceImage instance.
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
    return os.path.join('conference_images',zone, region, instance.territory.territory,dr_folder, filename)

class DrGiftCatalog(models.Model):
    """
    Model to represent a doctor's gift catalog.
    """
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='dr_gift_catalogs')
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Gift(models.TextChoices):
        GIFT1 = 'Pureit Classic 23 L', 'Pureit Classic 23 L'
        GIFT2 = 'Smart Watch Fastrack Reflex Rave FX', 'Smart Watch Fastrack Reflex Rave FX'
        GIFT3 = 'Kiam Marble Coated 7 pc Set', 'Kiam Marble Coated 7 pc Set'
        GIFT4 = 'Philips Blender 450W Daily Collection (HR2058/91)', 'Philips Blender 450W Daily Collection (HR2058/91)'
        GIFT5 = 'International Scientific Conference Registration', 'International Scientific Conference Registration'
    gift = models.CharField(max_length=255, choices=Gift.choices, default=Gift.GIFT1)
    conference_image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'dr_gift_catalogs'
        verbose_name = "Doctor Gift Catalog"
        verbose_name_plural = "Doctor Gift Catalogs"