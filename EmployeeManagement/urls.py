"""
URL configuration for EmployeeManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from Employee.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index, name='Index'),
    path('Registration', Registration, name='Registration'),
    path('Emp_log', Emp_log, name='Emp_log'),
    path('Emp_home', Emp_home, name='Emp_home'),
    path('Profile', Profile, name='Profile'),
    path('Logout', Logout, name='Logout'),
    path('Admin_Login', Admin_Login, name='Admin_Login'),
    path('Experience', Experience, name='Experience'),
]
