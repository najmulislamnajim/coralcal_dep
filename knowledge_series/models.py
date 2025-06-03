from django.db import models
from core.models import Territory

# Create your models here.
class BookWishes(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    dr_id = models.CharField(max_length=20, unique=True)
    dr_name = models.CharField(max_length=100, blank=True, null=True)
    class Book(models.TextChoices):
        BOOK1 = '100 diagnostic dilemmas in clinical medicine', '100 diagnostic dilemmas in clinical medicine'
        BOOK2 = '100 cases in obstetrics and gynaecology', '100 cases in obstetrics and gynaecology'
        BOOK3 = '100 cases in accute medicine', '100 cases in accute medicine'
    book = models.CharField(max_length=100, choices=Book.choices, default=Book.BOOK1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dr_name

    class Meta:
        db_table = 'book_wishes'
        verbose_name = "Book Wish"
        verbose_name_plural = "Book Wishes"