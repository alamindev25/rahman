from django.utils import timezone

from apps.system_setting.models import AboutSystem, SystemColor


def system_settings(request):
    system_info = AboutSystem.objects.first()
    system_color = (
        SystemColor.objects.filter(is_active=True)
        .values_list("code", flat=True)
        .first()
        or "#204452"
    )
    support_email = system_info.email if system_info else ""

    return {
        "system_info": system_info,
        "system_color": system_color,
        "support_email": support_email,
        "current_year": timezone.now().year,
    }
