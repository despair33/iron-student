from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import re_path
from django.contrib import admin


class AdminAccessMiddleware:
    """Ограничение доступа к /admin/ только для учителей"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_urls = [
            re_path(r'^admin/', admin.site.urls),
        ]
    
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/mainPage.html')
            
            if not request.user.is_superuser:
                if not request.user.groups.filter(name='Учитель').exists():
                    return HttpResponseRedirect('/mainPage.html')
        
        return self.get_response(request)