from django.contrib import admin
from .models import Comment, Work, Vote
# Register your models here.

@admin.register(Comment)
# esssential for ModelAdmin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'work', 'created_on')
    list_filter = ('created_on', 'work')
    search_fields = ('name', 'body')
    # actions = ['approve_comments']
    #
    # def approve_comments(self, request, queryset):
    #     queryset.update(active=True)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'type', 'rating', 'active')
    list_filter = ('active', 'pub_date', 'genre', 'type')
    search_fields = ('title', 'author', 'genre', 'type')
    actions = ['approve_works']

    def approve_works(self, request, queryset):
        queryset.update(active=True)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
        list_display = ('votedon', 'votedby')
