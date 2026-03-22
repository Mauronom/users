from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import Template


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dni", "uuid")
    search_fields = ("user__username", "dni")

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("html",)
    search_fields = ("html",)
