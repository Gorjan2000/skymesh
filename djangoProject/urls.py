"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.index, name=''),
    path('', views.index, name='/'),
    path('index/', views.index, name='index'),
    path('lightIntensity/', views.lightIntensityFromTable, name='lightIntensityFromTable'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('soil/', views.scrape_view, name='scrape'),
    path('test/', views.test_connection, name='test_connection'),
    path('map/', views.location_map, name='location_map'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
