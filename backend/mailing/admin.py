from django.contrib import admin
from .models import ContactModel, TemplateModel, MailModel

import uuid
from import_export import resources, fields

from import_export.admin import ImportExportModelAdmin

class ContactResource(resources.ModelResource):
    
    class Meta:
        model = ContactModel
        # No posar 'import_id_fields', així el CSV no necessita el UUID
        import_id_fields = ()
        fields = ('uuid','nom', 'mail', 'web', 'persona_contacte', 'telefon', 'notes', 'idioma')
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

        # Només mantenir columnes definides al Resource
        valid_fields = {f.column_name for f in self.get_fields()}
        keys_to_remove = [key for key in row.keys() if key not in valid_fields]
        for key in keys_to_remove:
            del row[key]

@admin.register(ContactModel)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ["nom", "mail", "idioma", "data_enviat"]
    search_fields = ["nom", "mail"]


@admin.register(TemplateModel)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["uuid", "subject","body"]


@admin.register(MailModel)
class MailAdmin(admin.ModelAdmin):
    list_display = ["uuid", "to", "status", "send_date","body"]
    list_filter = ["status"]
