from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin2/', admin.site.urls),
    path('admin/', include('admin_panel.urls'), name='admin_panel'),
    path('', include('blog_app.urls'), name='blog_app app'),
    path('ckeditor', include("ckeditor_uploader.urls")),
    # path('api/', include('api.urls'), name='api'),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)