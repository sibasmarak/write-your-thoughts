from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:author_id>/<slug:author_coolname>/create/', views.create, name='create'),
    path('<int:author_id>/<slug:author_coolname>/update/', views.update, name='update'),
    path('<int:author_id>/<slug:author_coolname>/addblog/', views.addblog, name='addblog'),
    path('<int:author_id>/<slug:author_coolname>/', views.detail_author, name='detail_author'),
    path('<int:author_id>/<slug:author_coolname>/subscribe/',views.subscribe, name='subscribe'),
    path('<int:author_id>/<slug:author_coolname>/unsubscribe/',views.unsubscribe, name='unsubscribe'),
    path('author/leaderboard/', views.author_leader, name='author_leader'),
    path('author/subscribed_Authors', views.subscribed_author_list, name='subscribed_author_list')
    # path('search/',views.search, name='search'),
    # path('<int:product_id>/upvote/', views.upvote, name='upvote'),
    # path('<int:product_id>/comment/', views.post_detail, name='comment'),
]
