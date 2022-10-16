from django.urls import path, include

from . import views
# app_name = 'classlist'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.view_home, name='home'),
    path('accounts/', include('allauth.urls')),  # Includes all django-allauth URL's
    path('login/', views.view_name, name="view_name"),
    path('list/', views.ClassView.as_view(), name='list')
]