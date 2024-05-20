from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import handler404

from core.views import frontpage, about, custom_404

handler404 = 'core.views.custom_404'

urlpatterns = [
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('userprofile.urls')),
    path('', include('storefront.urls')),
    path('', frontpage, name='frontpage'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


