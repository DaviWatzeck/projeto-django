from django.contrib import admin

from .models import Category, Receita


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
