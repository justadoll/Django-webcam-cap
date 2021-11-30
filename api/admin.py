from django.contrib import admin
from .models import Uri_link

class UrlAdmin(admin.ModelAdmin):
    list_display = ('name','url','ip','create_date')
    list_display_links = ('name','url')
    search_fields = ('name','url', 'ip')

admin.site.register(Uri_link, UrlAdmin)
