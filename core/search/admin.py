from django.contrib import admin
from .models import Material, Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'file_name', 'date_publication', 'visibility',)
    list_filter = ('visibility', 'title', 'author')

