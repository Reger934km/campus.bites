from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create a superuser for production deployment'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@campusbites.app'
        password = 'CampusBites#Admin2025!'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists.')
            )
            return
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create superuser: {e}')
            )
            # Fallback to interactive creation
            call_command('createsuperuser', interactive=False)
