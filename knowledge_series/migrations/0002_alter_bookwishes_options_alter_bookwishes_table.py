# Generated by Django 5.2.1 on 2025-06-03 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_series', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookwishes',
            options={'verbose_name': 'Book Wish', 'verbose_name_plural': 'Book Wishes'},
        ),
        migrations.AlterModelTable(
            name='bookwishes',
            table='book_wishes',
        ),
    ]
