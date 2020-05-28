from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include('gas.api.urls')),
    path('', include('gas.pages.urls')),
    path('auth/', include('gas.person.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
