from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    ordering = ('title',)
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'publication_year')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )