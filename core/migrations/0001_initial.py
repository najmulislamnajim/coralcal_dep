# Generated by Django 5.2.1 on 2025-06-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Territory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territory', models.CharField(max_length=10, unique=True)),
                ('territory_name', models.CharField(max_length=100)),
                ('region_name', models.CharField(max_length=100)),
                ('zone_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Territory',
                'verbose_name_plural': 'Territories',
                'db_table': 'rpl_territory',
            },
        ),
    ]
