from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from work import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('thoughts/leaderboard', views.thought_leaderboard, name='thought'),
    path('poems/leaderboard', views.poems_leaderboard, name='poems'),
    path('stories/leaderboard', views.stories_leaderboard, name='stories'),
    path('fiction/leaderboard', views.fiction_leaderboard, name='fiction'),
    path('non_fiction/leaderboard', views.non_fiction_leaderboard, name='non_fiction'),
    path('accounts/', include('accounts.urls')),
    path('work/', include('work.urls')),
    path('author/', include('author.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
