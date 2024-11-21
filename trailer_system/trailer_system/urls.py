"""
URL configuration for trailer_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from authentication.views import (
    home_view,
    main_dashboard,
    trailer_list,
    add_trailer,
    edit_trailer,
    delete_trailer
  
)

from authentication.views import custom_logout,CustomLoginView  # Import only custom_logout for testing


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),  # Include auth views
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('', home_view, name='home'),  # Add the homepage URL pattern
    path('dashboard/', main_dashboard, name='main-dashboard'),
    path('trailers/', trailer_list, name='trailer-list'),  # Trailer list URL
    path('trailers/add/', add_trailer, name='add-trailer'),  # Add trailer URL
    path('trailers/edit/<int:trailer_id>/', edit_trailer, name='edit-trailer'),  # Edit trailer URL
    path('trailers/delete/<int:trailer_id>/', delete_trailer, name='delete-trailer'),  # Delete trailer URL
    path('custom-logout/', custom_logout, name='custom-logout'),  # Custom logout URL


]
