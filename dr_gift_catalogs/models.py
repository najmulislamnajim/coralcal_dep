from django.db import models
from core.models import Territory

# Create your models here.
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
    conference_image = models.ImageField(upload_to='conference_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dr_name} - ({self.territory})"
    
    class Meta:
        db_table = 'dr_gift_catalogs'
        verbose_name = "Doctor Gift Catalog"
        verbose_name_plural = "Doctor Gift Catalogs"