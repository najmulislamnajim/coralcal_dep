from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('territory', 'Territory'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
        ('zone', 'Zone'),
        ('region', 'Region')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    zone_name = models.CharField(max_length=100, blank=True, null=True)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username + self.user_type
    
class Territory(models.Model):
    """
    Model to store Territory.

    Attributes:
        territory (CharFiled): Territory code (unique).
        territory_name (CharField): Name of the territory (mandatory).
        region_name (CharField): Name of the region (mandatory).
        zone_name (CharField): Name of the zone (mandatory).
    """
    territory = models.CharField(max_length=10, unique=True)
    territory_name = models.CharField(max_length=100)
    region_name = models.CharField(max_length=100)
    zone_name = models.CharField(max_length=100)

    def __str__(self):
        return self.territory_name

    class Meta:
        db_table = 'rpl_territory' 
        verbose_name = 'Territory'
        verbose_name_plural = 'Territories'
