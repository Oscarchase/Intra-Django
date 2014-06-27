from django.contrib import admin
from auth.models import DogeUser

class DogeUserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'mail', 'picture_as_html')
    readonly_fields = ('picture_as_html',)
    search_fields = ['login', 'first_name', 'last_name', 'phone', 'mail']
    list_display = ['login', 'first_name', 'last_name', 'birth_date']

admin.site.register(DogeUser, DogeUserAdmin)
