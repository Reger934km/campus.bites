from django.apps import AppConfig


class CanteenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'canteen'

    def ready(self):
        # Import here to avoid circular imports
        import os
        if os.environ.get('RUN_MAIN', None) != 'true':
            from django.contrib.auth.models import User
            from django.db import IntegrityError
            
            # Create superuser if it doesn't exist
            try:
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@campusbites.app',
                        password='CampusBites#Admin2025!'
                    )
                    print("✅ Superuser 'admin' created successfully!")
                else:
                    print("✅ Superuser 'admin' already exists!")
            except IntegrityError:
                print("⚠️ Superuser creation failed - may already exist")
            except Exception as e:
                print(f"❌ Error creating superuser: {e}")
