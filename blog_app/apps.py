from django.apps import AppConfig
from django.core.signals import request_finished


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_app'

    def ready(self):

        from . import signals
