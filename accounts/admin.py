from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

#Sets what is visible in admin panel (hides password)
class AccountAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "username", "date_joined", "last_login", "is_active")
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)