from django.contrib import admin
from .models import Material, Tag, Reference

# Register your models here.
# Admin panel, no docs please
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'file_name', 'date_publication', 'visibility',)
    list_filter = ('visibility', 'title', 'author')


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass
