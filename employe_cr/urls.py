"""
URL configuration for employe_cr project.

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
from cr import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.SignInView.as_view(),name="login"),
    path("index",views.Index.as_view(),name="index"),
    path("employees/add",views.EmployeeCreateView.as_view(),name="emp_add"),
    path("employees/all",views.EmployeeListView.as_view(),name="emp_all"),
    path("emloyees/<int:pk>/details",views.EmployeeDetailView.as_view(),name="emp_details"),
    path("emloyees/<int:pk>/update",views.EmployeeUpdateView.as_view(),name="emp_update"),
    path("emloyees/<int:pk>/delete",views.EmployeeDeleteView.as_view(),name="emp_delete"),
    path("signup",views.SingpuView.as_view(),name="register"),
    path("logout",views.SingOutView.as_view(),name="logout")
   
]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

