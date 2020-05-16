from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:work_id>/<slug:work_slug>/', views.detail, name='detail'),
    path('<int:work_id>/<slug:work_slug>/delete/', views.delete, name='delete'),
    path('search/',views.search, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    path('<int:work_id>/<slug:work_slug>/comment/', views.comment, name='comment'),
    path('<int:work_id>/<slug:work_slug>/<int:comment_id>/delete_comment', views.delete_comment, name='delete_comment'),
    path('<int:work_id>/<slug:work_slug>/rate', views.rate, name='rate'),
]
