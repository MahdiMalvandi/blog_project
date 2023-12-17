from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


def only_managers(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'errors/403.html')

    return _wrapped_view
