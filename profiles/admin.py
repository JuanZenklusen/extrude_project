from django.contrib import admin
from .models import Profile, Contact

admin.site.register(Profile)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'created_at', 'modified_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at', 'modified_at')
    readonly_fields = ('name', 'phone', 'email', 'subject', 'consult', 'created_at', 'modified_at')

admin.site.register(Contact, ContactAdmin)