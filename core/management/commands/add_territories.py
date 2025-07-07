from django.core.management.base import BaseCommand
from core.models import Territory 
import os 
from django.conf import settings
import pandas as pd

class Command(BaseCommand):
    help = 'Add territories to the database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--file_path',
            type=str,
            default= os.path.join(settings.BASE_DIR,'core','data', 'territories.xlsx'),
            help='Path to the Excel file (default: core/data/territories.xlsx)'
        )
    
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        try:
            df = pd.read_excel(file_path)
            created_count = 0
            updated_count = 0
            
            # Iterate through rows
            for _, row in df.iterrows():
                # ZoneName RegionName SAPAreaCode AreaName
                territory_data = {
                    'zone_name': row.get('ZoneName', ''),
                    'region_name': row.get('RegionName', ''),
                    'territory': row.get('SAPAreaCode', ''),
                    'territory_name': row.get('AreaName', ''),
                }
                
                # Create or update territory
                territory, created = Territory.objects.update_or_create(
                    territory=territory_data['territory'],
                    defaults=territory_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"Created territory: {territory}")
                else:
                    updated_count += 1
                    self.stdout.write(f"Updated territory: {territory}")
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully processed {len(df)} territories: "
                    f"{created_count} created, {updated_count} updated"
                )
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR(f'File is empty: {file_path}'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file: {file_path}'))
            self.stdout.write(self.style.ERROR(str(e)))
            return