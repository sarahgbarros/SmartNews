from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('date_joined',)


admin.site.register(User, UserAdmin)
