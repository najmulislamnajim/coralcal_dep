from django.db import models

# Create your models here.
class AccessControl(models.Model):
    key=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'access_control'
        verbose_name = 'Access Control'
        verbose_name_plural = 'Access Control'
        
    def __str__(self):
        return self.key+"-"+str(self.is_active)