from django.db import models
from core.models import Territory

# Create your models here.
class DoctorOpinion(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='doctor_opinions')
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100)
    dr_phone = models.CharField(max_length=15)
    dr_address = models.CharField(max_length=255)
    dr_specialty = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor_opinion'
        verbose_name = 'Doctor Opinion'
        verbose_name_plural = 'Doctor Opinions'
        
    def __str__(self):
        return f"{self.dr_name} ({self.dr_specialty})"
    
class DoctorIndication(models.Model):
    doctor_opinion = models.ForeignKey(DoctorOpinion, on_delete=models.CASCADE, related_name='indications')
    indication_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor_indication'
        verbose_name = 'Doctor Indication'
        verbose_name_plural = 'Doctor Indications'
        
    def __str__(self):
        return f"Indication for {self.doctor_opinion.dr_name}"