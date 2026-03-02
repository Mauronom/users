from django.contrib import admin

# Register your models here.
from .models import Profile


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dni", "uuid")
    search_fields = ("user__username", "dni")