from django.db import models

# Create your models here.
class Territory(models.Model):
    """
    Model to store Terriotory.

    Attributes:
        territory (CharFiled): Territory code (unique).
        territory_name (CharField): Name of the terrytory (mandatory).
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
