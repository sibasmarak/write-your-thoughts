from django.contrib import admin
from .models import Author, Blog
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('coolname', 'rating', 'active')
    list_filter = ('active','rating')
    search_fields = ('coolname',)
    actions = ['approve_author']

    def approve_author(self, request, queryset):
        queryset.update(active=True)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'url', 'sitename')
    list_filter = ('author','sitename')
    search_fields = ('author', 'url', 'sitename')
    
    # actions = ['approve_author']
    #
    # def approve_author(self, request, queryset):
    #     queryset.update(active=True)
