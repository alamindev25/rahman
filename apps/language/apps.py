from django.apps import AppConfig
from django.db.models.signals import post_migrate


def auto_seed_languages(sender, **kwargs):
    try:
        from .seed_data import seed_languages
        seed_languages()
    except Exception as e:
        print("Auto seed error:", e)


class LanguageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.language'

    def ready(self):
        try:
            from django.db import connection
            tables = connection.introspection.table_names()
            if 'language_language' not in tables:
                print("Creating language_language table via auto-migrate...")
                from django.core.management import call_command
                call_command('migrate', 'language')
        except Exception as e:
            print("Auto-migrate error:", e)

        post_migrate.connect(auto_seed_languages, sender=self)
