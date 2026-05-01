"""
URL configuration for iron-student project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

def root_view(request):
    return HttpResponseRedirect('/mainPage.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('', root_view),
    # Отдача HTML-файлов из frontend/
    path('index.html', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'index.html'}),
    path('mainPage.html', serve, {'document_root': settings.BASE_DIR.parent / 'frontend', 'path': 'mainPage.html'}),
]

if settings.DEBUG:
    # Статические файлы (CSS, JS) из frontend/
    urlpatterns += static('/static/', document_root=settings.BASE_DIR.parent / 'frontend')
