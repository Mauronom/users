from django.contrib import admin
from hex.mailing.domain.mail import MailStatus
from .models import ContactModel, TemplateModel, MailModel
from django_summernote.admin import SummernoteModelAdmin

import uuid
from import_export import resources, fields

from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm
from django import forms
from hex.mailing.app import CreateMail
from hex.mailing.infra import c_bus

@admin.action(description="Create initial mail")
def create_initial_mail(modeladmin, request, queryset):
    for contact in queryset:
        if contact.data_enviat:
            obj, created = MailModel.objects.get_or_create(
                contact=contact,
                defaults={"uuid": str(uuid.uuid4()), "send_date": contact.data_enviat, "subject": "init", "body": "init","status": MailStatus.sent.value},
            )

@admin.action(description="Create email from template")
def create_email_from_template(modeladmin, request, queryset):
    template = TemplateModel.objects.filter(subject="Test")[0]
    for contact in queryset:
        c_bus.dispatch(CreateMail(template_id=template.uuid, contact_id=contact.uuid))


class ContactImportForm(ImportForm):
    tags = forms.CharField(required=False, help_text="Tags per a tots els contactes importats")

class ContactResource(resources.ModelResource):

    def before_import(self, dataset, **kwargs):
        self._tags = kwargs.get('user_form_data', {}).get('tags', '')

    class Meta:
        model = ContactModel
        # No posar 'import_id_fields', així el CSV no necessita el UUID
        import_id_fields = ()
        fields = ('uuid','nom', 'mail', 'web', 'persona_contacte', 'telefon', 'notes', 'idioma',"tags","data_enviat")
        skip_unchanged = False
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # Generar UUID automàtic
        if 'uuid' not in row or not row.get('uuid'):
            row['uuid'] = str(uuid.uuid4())

        # Mapar idioma textual a codi curt
        idioma_map = {
            'català': 'ca',
            'castellà': 'es',
            'english': 'en',
            'ca': 'ca',
            'es': 'es',
            'en': 'en'
        }
        if 'idioma' in row:
            valor = row['idioma'].strip().lower()
            row['idioma'] = idioma_map.get(valor, 'ca')  # default 'ca' si no troba

        # Apliquem els tags del formulari
        row['tags'] = getattr(self, '_tags', '')

        # Només mantenir columnes definides al Resource
        valid_fields = {f.column_name for f in self.get_fields()}
        keys_to_remove = [key for key in row.keys() if key not in valid_fields]
        for key in keys_to_remove:
            del row[key]

@admin.register(ContactModel)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    import_form_class = ContactImportForm
    list_display = ["nom", "mail", "idioma", "data_enviat"]
    search_fields = ["nom", "mail"]
    actions = [create_initial_mail, create_email_from_template]
    

@admin.register(TemplateModel)
class TemplateAdmin(SummernoteModelAdmin):
    list_display = ["subject"]
    summernote_fields = ['body',]


@admin.register(MailModel)
class MailAdmin(SummernoteModelAdmin):
    list_display = ["subject","contact", "status", "send_date"]
    list_filter = ["status"]
    summernote_fields = ['body',]

