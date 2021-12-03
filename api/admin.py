from django.contrib import admin
from .models import Uri_link

class UrlAdmin(admin.ModelAdmin):
    list_display = ('name','url','get_ips','ip','create_date')
    list_display_links = ('name','url')
    search_fields = ('name','url', 'ip','get_ips')

admin.site.register(Uri_link, UrlAdmin)
