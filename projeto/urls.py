"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path

# HTTP REQUEST <- HTTP RESPONSE

# HTTP REQUEST


def home(request):
    return HttpResponse('HOME')
    # HTTP RESPONSE


def sobre(request):
    return HttpResponse('sobre')
    # HTTP RESPONSE


def contato(request):
    return HttpResponse('contato')
    # HTTP RESPONSE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # Home
    path('sobre/', sobre),  # /sobre/
    path('contato/', contato),  # /contato/
]