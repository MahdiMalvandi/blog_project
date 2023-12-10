from django.http import HttpResponseForbidden
from django.shortcuts import render


class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_superuser:
            return render(request, 'admin_panel/401.html')
        return self.get_response(request)
