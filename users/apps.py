from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        #django doc recommends doing it this way instead of creating signals.py in blog app to avoid some side affects with import
