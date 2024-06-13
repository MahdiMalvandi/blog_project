from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
                  path('django-admin/', admin.site.urls),
                  path('admin/', include('admin_panel.urls'), name='admin_panel'),
                  path('', include('blog_app.urls'), name='blog_app app'),
                  path('ckeditor', include("ckeditor_uploader.urls")),
                  path('api-auth/', include('rest_framework.urls')),
                  re_path(r'^images/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
