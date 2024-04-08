from django.contrib import admin

from .models import Category, Receita


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author',]
    list_display_links = 'title',
    search_fields = 'id', 'title', 'description', 'slug', 'preparations_steps',
    list_filter = 'category', 'author', 'is_published', \
        'preparations_steps_is_html',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)
