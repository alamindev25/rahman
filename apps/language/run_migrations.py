import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command
from apps.language.seed_data import seed_languages

print("Running migrations...")
call_command('migrate', 'language')
print("Seeding languages...")
seed_languages()

print("Done!")
