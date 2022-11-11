from django.urls import path, include

from . import views
# app_name = 'classlist'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.view_home, name='home'),
    path('accounts/', include('allauth.urls')),  # Includes all django-allauth URL's
    path('login/', views.view_name, name="view_name"),
    path('list/', views.get_depts, name='list'),
    path('list/<str:dept_abbr>/', views.load_dept_courses_from_db, name='get_courses_by_dept'),
    path('view_users/', views.ViewUsers.as_view(), name='view_users'),
    path('view_users/send_friend_request/<int:userID>', views.send_friend_request, name='send friend request submit'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('deny_friend_request/<int:requestID>/', views.deny_friend_request, name='deny friend request'),
    path('remove_friend/<int:requestID>/', views.remove_friend, name='remove friend'),
    path('my_account/', views.ViewAccount.as_view(), name='my_account'),
    path('create_account/', views.create_account, name='create account'),
    path('schedule/', views.schedule_view, name ='schedule'),
    path('delete_course/', views.delete_course, name='delete_course'),
]