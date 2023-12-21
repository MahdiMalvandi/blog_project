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
    """

    :param required_permission:
     'app_name.view_permissions' like 'blog_app.view_post'
    :param message:
    the message you want to display
    :return:
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_anonymous:
                return view_func(request, *args, **kwargs)
            else:
                if required_permission in request.user.get_user_permissions():
                    return view_func(request, *args, **kwargs)
                else:
                    if request.user.is_staff:
                        user = 'admin'
                    else:
                        user = 'normal'
                    context = {
                        'custom_message': message,
                        'user_type': user
                    }
                    return render(request, 'errors/403.html', context=context, status=403)

        return wrapper

    return decorator
