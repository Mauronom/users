from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact

from import_export import resources
from .models import Contact

import uuid
from import_export import resources, fields
from .models import Contact

import uuid
from import_export import resources
from .models import Contact
from import_export.admin import ImportExportModelAdmin

class ContactResource(resources.ModelResource):
    email = fields.Field(column_name='mail', attribute='email')  # mapar mail → email

    class Meta:
        model = Contact
        # No posar 'import_id_fields', així el CSV no necessita el UUID
        import_id_fields = ()
        fields = ('nom', 'email', 'web', 'persona_contacte', 'telefon', 'notes', 'idioma')
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
@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource

    # Camps que es veuran a la llista
    list_display = ('nom', 'email', 'telefon', 'persona_contacte', 'idioma')
    
    # Camps que es podran clicar per anar al detall
    list_display_links = ('nom', 'email')
    
    # Filtres laterals
    list_filter = ('idioma',)
    
    # Camps que es podran buscar
    search_fields = ('nom', 'email', 'persona_contacte', 'telefon')
    
    # Orden per defecte
    ordering = ('nom',)
    
    # Camps opcions en la vista de detall
    fieldsets = (
        (None, {
            'fields': ('nom', 'email', 'web', 'persona_contacte', 'telefon', 'notes', 'idioma')
        }),
    )