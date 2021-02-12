from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Arena.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
