from django.urls import path, include
from . import views
from author import views as author_views
from work import views as work_views

urlpatterns = [
    path('signup/info', views.signup_info, name='signup_info'),
    path('signup/normalUser', views.signup_as_user, name='signup_user'),
    path('signup/author', author_views.signup_as_author, name='signup_author'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('convert/', views.convert_author, name='convert_author'),
    path('forget/', views.forget, name='forget'),
]
