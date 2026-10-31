from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from apps.system_setting.admin_profile import update_profile


def get_about_system():
    from apps.system_setting.models import AboutSystem
    return AboutSystem.objects.first()

def get_system_title():
    about_system = get_about_system()
    if about_system and about_system.title:
        return about_system.title
    return "Admin"
    
def get_system_file_url(field_name):
    about_system = get_about_system()
    if not about_system:
        return ""

    file_field = getattr(about_system, field_name, None)
    if file_field:
        return file_field.url
    return ""

def get_unfold_settings():
    return {
        "SITE_TITLE": lambda request: get_system_title(),
        "SITE_HEADER": lambda request: get_system_title(),
        # "SITE_SUBHEADER": lambda request: get_about_system().title,
        "SITE_URL": "/",
        "SITE_ICON": {
            "light": lambda request: get_system_file_url("logo"), 
            "dark": lambda request: get_system_file_url("logo"),  
        },
        "SITE_SYMBOL": "speed", 
        "SITE_FAVICONS": [
            {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: get_system_file_url("favicon"),
            },
        ],
        "DASHBOARD_CALLBACK": "apps.dashboard.views.dashboard_callback",

        "SHOW_HISTORY": True,  
        "SHOW_VIEW_ON_SITE": True,  
        "SHOW_BACK_BUTTON": True, 
        "LOGIN": {
            "image": lambda request: static("sample/login-bg.jpg"),
            "redirect_after": lambda request: reverse_lazy("admin:index"),
        },
        "BORDER_RADIUS": "6px",
        "SIDEBAR": {
            "show_search": True, 
            "show_all_applications": True,  
            "navigation": [
                {
                    "items": [
                        {
                            "title": _("Dashboard"),
                            "icon": "dashboard",
                            "link": reverse_lazy("admin:index"),
                            "permission": lambda request: request.user.is_superuser,
                        },
                    ],
                },
                {
                    "title": _("User Management"),
                    "separator": True, 
                    "collapsible": True,  
                    "items": [
                        {
                            "title": _("Users"),
                            "icon": "people",
                            "link": reverse_lazy("admin:user_user_changelist"),
                        },
                        {
                            "title": _("ClinicAdmins"),
                            "icon": "people",
                            "link": reverse_lazy("admin:clinic_clinicregister_changelist"),
                        },
                    ],
                },
                {
                    "title": _("Clinic Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Clinic Registers"),
                            "icon": "local_hospital",
                            "link": reverse_lazy("admin:clinic_clinicregister_changelist"),
                        },
                        {
                            "title": _("Clinic Profiles"),
                            "icon": "badge",
                            "link": reverse_lazy("admin:clinic_clinicprofile_changelist"),
                        },
                        {
                            "title": _("Clinic Images"),
                            "icon": "image",
                            "link": reverse_lazy("admin:clinic_clinicimage_changelist"),
                        },
                        {
                            "title": _("Clinic Insurance"),
                            "icon": "shield",
                            "link": reverse_lazy("admin:clinic_clinicinsurance_changelist"),
                        },
                        {
                            "title": _("Clinic Treatments"),
                            "icon": "medical_services",
                            "link": reverse_lazy("admin:clinic_clinictreatment_changelist"),
                        },
                        {
                            "title": _("Clinic Facilities"),
                            "icon": "checklist",
                            "link": reverse_lazy("admin:clinic_clinicfacility_changelist"),
                        },
                        {
                            "title": _("Accepted Patients"),
                            "icon": "groups",
                            "link": reverse_lazy("admin:clinic_clinicacceptedpatients_changelist"),
                        },
                        {
                            "title": _("Payment Methods"),
                            "icon": "payments",
                            "link": reverse_lazy("admin:clinic_clinicpaymentmethod_changelist"),
                        },
                        {
                            "title": _("Availability"),
                            "icon": "event_available",
                            "link": reverse_lazy("admin:clinic_clinicavailability_changelist"),
                        },
                        {
                            "title": _("Ratings"),
                            "icon": "star",
                            "link": reverse_lazy("admin:clinic_clinicrating_changelist"),
                        },
                        {
                            "title": _("appoinment"),
                            "icon": "star",
                            "link": reverse_lazy("admin:appoinment_clinicappointment_changelist"),
                        },
                        {
                            "title": _("Clinic Slot Capacity"),
                            "icon": "event_seat",
                            "link": reverse_lazy("admin:appoinment_clinicslotcapacity_changelist"),
                        },
                        {
                            "title": _("Appointment Payments"),
                            "icon": "payments",
                            "link": reverse_lazy("admin:payment_appointmentpayment_changelist"),
                        },
                        # {
                        #     "title": _("TreatmentSchedule"),
                        #     "icon": "event_seat",
                        #     "link": reverse_lazy("admin:appoinment_treatmentschedule_changelist"),
                        # },
                    ],
                },
                {
                    "title": _("Payment Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Appointment Payments"),
                            "icon": "payments",
                            "link": reverse_lazy("admin:payment_appointmentpayment_changelist"),
                        },
                    ],
                },
                {
                    "title": _("Blog"),
                    "separator": True, 
                    "collapsible": True,  
                    "items": [
                        {
                            "title": _("Blog Posts"),
                            "icon": "people",           
                            "link": reverse_lazy("admin:blog_blogpost_changelist"),
                        },
                
                    ],
                },
                {
                    "title": _("Contact"),
                    "separator": True,
                    "collapsible": True,  
                    "items": [
                        {
                            "title": _("ContactInfo"),
                            "icon": "people",           
                            "link": reverse_lazy("admin:contact_contactinfo_changelist"),
                        },
                        {
                            "title": _("ContactMessage"),
                            "icon": "people",           
                            "link": reverse_lazy("admin:contact_contactmessage_changelist"),
                        },  
                    ],
                },
                 {
                    "title": _("Language"),
                    "separator": True,  
                    "collapsible": True, 
                    "items": [
                        {
                            "title": _("Language"),
                            "icon": "language",           
                            "link": reverse_lazy("admin:language_language_changelist"),
                        },
                    ],
                },
                {
                    "title": _("About-Us"),
                    "separator": True,  # Top border
                    "collapsible": True,  # Collapsible group of links
                    "items": [
                         {
                            "title": _("About Banners"),
                            "icon": "analytics",
                            "link": reverse_lazy("admin:about_us_aboutbanner_changelist"),
                        },
                         {
                            "title": _("About Heros"),
                            "icon": "   analytics",
                            "link": reverse_lazy("admin:about_us_abouthero_changelist"),
                        },
                        {
                            "title": _("Statistics"),
                            "icon": "analytics",
                            "link": reverse_lazy("admin:about_us_statistic_changelist"),
                        },
                        {
                            "title": _("Team Members"),
                            "icon": "groups",
                            "link": reverse_lazy("admin:about_us_teammember_changelist"),
                        },
                        {
                            "title": _("Why Choose Us"),
                            "icon": "help",
                            "link": reverse_lazy("admin:about_us_whychooseus_changelist"),
                        },
                        {
                            "title": _("Mission & Vision"),
                            "icon": "flag",
                            "link": reverse_lazy("admin:about_us_missionvision_changelist"),
                        },
                    ],
                },
                {
                    "title": _("Resources"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Resource Items"),
                            "icon": "folder",
                            "link": reverse_lazy("admin:resources_resourceitem_changelist"),
                        },
                        {
                            "title": _("Planning Checklists"),
                            "icon": "checklist",
                            "link": reverse_lazy("admin:resources_planningchecklist_changelist"),
                        },
                    ],
                },
                {
                    "title": _("System Setting"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Update Profile"),
                            "icon": "edit",
                            "link": lambda req: update_profile(req),
                        },
                        {
                            "title": _("About System"),
                            "icon": "info",
                            "link": reverse_lazy(
                                "admin:system_setting_aboutsystem_changelist"
                            ),
                        },
                        {
                            "title": _("Social Media"),
                            "icon": "share",
                            "link": reverse_lazy(
                                "admin:system_setting_socialmedia_changelist"
                            ),
                        },
                        {
                            "title": _("SMTP Settings"),
                            "icon": "email",
                            "link": reverse_lazy(
                                "admin:system_setting_smtpsetting_changelist"
                            ),
                        },
                        {
                            "title": _("System Color"),
                            "icon": "palette",
                            "link": reverse_lazy(
                                "admin:system_setting_systemcolor_changelist"
                            ),
                        }
                    ],
                },
                {
                    "title": _("Page Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Pages"),
                            "icon": "pages",
                            "link": reverse_lazy("admin:cms_page_changelist"),
                        },
                    ],
                },
                {
                    "title": _("CMS Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("CMS"),
                            "icon": "auto_stories",
                            "link": reverse_lazy("admin:cms_cms_changelist"),
                        },
                    ],
                },
                {
                    "title": _("FAQ Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("FAQs"),
                            "icon": "help",
                            "link": reverse_lazy("admin:cms_faq_changelist"),
                        },
                    ],
                }
            ],
        },
    }
