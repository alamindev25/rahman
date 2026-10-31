"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path , include, re_path
from django.conf.urls.static import static
from project import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('apps.user.urls')),
    path('api/', include('apps.clinic.urls')),
    path('api/', include('apps.system_setting.urls')),
    path('api/', include('apps.social_auth.urls')),
    path('api/', include('apps.subscription.urls')),
    path('api/', include('apps.notification.urls')),
    path('api/', include('apps.cms.urls')),
    path('api/', include('apps.appoinment.urls')),
    path('api/', include('apps.blog.urls')),
    path('api/', include('apps.contact.urls')), 
    path('api/', include('apps.language.urls')), 
    path('api/', include('apps.about_us.urls')),
    path('api/', include('apps.payment.urls')),
    path('api/', include('apps.resources.urls')),           
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


urlpatterns += [
    path("", admin.site.urls),
]