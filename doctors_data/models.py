from django.db import models

# Create your models here.
class Doctor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    Designation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        
class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=55)
    division = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    upazila = models.CharField(max_length=255)
    thana = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doctor.name + ' ' + self.address
    class Meta:
        db_table = 'chambers'
        verbose_name = 'Chamber'
        verbose_name_plural = 'Chambers'