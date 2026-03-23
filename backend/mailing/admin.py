from django.contrib import admin
from .models import ContactModel, TemplateModel, MailModel


@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["nom", "mail", "idioma", "data_enviat"]
    search_fields = ["nom", "mail"]


@admin.register(TemplateModel)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["uuid", "subject","body"]


@admin.register(MailModel)
class MailAdmin(admin.ModelAdmin):
    list_display = ["uuid", "to", "status", "send_date","body"]
    list_filter = ["status"]
