from django.urls import path

from . import views
app_name = 'classlist'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.ClassView.as_view(), name='list')
]
