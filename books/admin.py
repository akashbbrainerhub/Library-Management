from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'quantity', 'is_available', 'created_by')
    list_filter = ('is_available', 'category')
    search_fields = ('title', 'author', 'isbn')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()