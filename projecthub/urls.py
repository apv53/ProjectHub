from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects import views as project_views

urlpatterns = [
    path('', project_views.project_home, name='home'),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),   # include app urls here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)