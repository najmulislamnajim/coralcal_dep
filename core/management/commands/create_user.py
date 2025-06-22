from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Territory, UserProfile

class Command(BaseCommand):
    help = 'Create users for each territory and an admin user'

    def handle(self, *args, **kwargs):
        # Create users for territories
        territories = Territory.objects.all()
        default_password = 'coralcal'
        for territory in territories:
            username = territory.territory
            if not User.objects.filter(username=username).exists():
                user =User.objects.create_user(
                    username=username,
                    password=default_password
                )
                UserProfile.objects.create(
                    user=user,
                    user_type='territory'
                )
                self.stdout.write(self.style.SUCCESS(f'Created user for {username}'))
            else:
                user = User.objects.get(username=username)
                UserProfile.objects.create(
                    user=user,
                    user_type='territory'
                )
                self.stdout.write(f'User {username} already exists')

        # Create admin user
        admin_username = 'admin'
        admin_password = 'coralcal@123'
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                email='admin@example.com'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            user = User.objects.get(username=admin_username)
            user.set_password(admin_password)
            user.save()
            self.stdout.write('Admin user already exists')
            
        # Create zone users 
        for zone in Territory.objects.values_list('zone_name', flat=True).distinct():
            username = zone.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=default_password)
                UserProfile.objects.create(user=user, user_type='zone', zone_name=zone)
                self.stdout.write(self.style.SUCCESS(f'Created zone user: {username}'))
        
        # Region Users
        for region in Territory.objects.values_list('region_name', flat=True).distinct():
            username = region.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=default_password)
                UserProfile.objects.create(user=user, user_type='region', region_name=region)
                self.stdout.write(self.style.SUCCESS(f'Created region user: {username}'))