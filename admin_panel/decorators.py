from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.shortcuts import render
from functools import wraps


def only_managers(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'errors/403.html')

    return _wrapped_view


def custom_permission_required(required_permission, message):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.has_perm(required_permission):
                return view_func(request, *args, **kwargs)
            else:
                context = {
                    'custom_message': message
                }
                return render(request, 'errors/403.html', context=context, status=403)

        return wrapper

    return decorator
