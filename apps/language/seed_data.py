from .models import Language


def seed_languages():
    languages = [
        {'code': 'en', 'name': 'English', 'native_name': 'English', 'direction': 'ltr', 'is_default': True},
        {'code': 'zh-hans', 'name': 'Mandarin Chinese', 'native_name': '中文 (简体)', 'direction': 'ltr', 'is_default': False},
        {'code': 'hi', 'name': 'Hindi', 'native_name': 'हिन्दी', 'direction': 'ltr', 'is_default': False},
        {'code': 'es', 'name': 'Spanish', 'native_name': 'Español', 'direction': 'ltr', 'is_default': False},
        {'code': 'fr', 'name': 'French', 'native_name': 'Français', 'direction': 'ltr', 'is_default': False},
        {'code': 'ru', 'name': 'Russian', 'native_name': 'Русский', 'direction': 'ltr', 'is_default': False},
        {'code': 'ur', 'name': 'Urdu', 'native_name': 'اردو', 'direction': 'rtl', 'is_default': False},
        {'code': 'id', 'name': 'Indonesian', 'native_name': 'Bahasa Indonesia', 'direction': 'ltr', 'is_default': False},
        {'code': 'bn', 'name': 'Bengali', 'native_name': 'বাংলা', 'direction': 'ltr', 'is_default': False},
    ]

    for item in languages:
        Language.objects.get_or_create(
            code=item['code'],
            defaults={
                'name': item['name'],
                'native_name': item['native_name'],
                'direction': item['direction'],
                'is_active': True,
                'is_default': item['is_default'],
            }
        )
    print("Languages seeded successfully.")
