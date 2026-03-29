from django.contrib import admin
from django.contrib.admin import helpers
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.conf import settings
from hex.mailing.domain.mail import MailStatus
from .models import ContactModel, TemplateModel, MailModel
from django_summernote.admin import SummernoteModelAdmin

import uuid
import os
from import_export import resources, fields

from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm
from django import forms
from .forms import SelectTemplateForm
from hex.mailing.app import CreateMail, SendMail, CreateTemplateFromHtml
from hex.mailing.infra import c_bus
from .html_utils import extract_substitutions, extract_cids, render_body_with_inline_images

CONTACT_FIELDS = ["nom", "mail", "web", "persona_contacte", "telefon", "notes", "data_enviat", "idioma", "tags"]
HTML_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "html_templates")
IMG_DIR = os.path.join(os.path.dirname(__file__), "img")

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
    form = SelectTemplateForm(request.POST or None)
    if 'apply' in request.POST and form.is_valid():
        template = form.cleaned_data['template']
        for contact in queryset:
            c_bus.dispatch(CreateMail(template_id=template.uuid, contact_id=contact.uuid))
        return None
    return render(request, 'mailing/select-template.html', {
        'form': form,
        'queryset': queryset,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    })


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
    change_list_template = "mailing/template_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("create-from-html/", self.admin_site.admin_view(self.select_html_view), name="mailing_template_create_from_html"),
            path("create-from-html/map/", self.admin_site.admin_view(self.map_fields_view), name="mailing_template_map_fields"),
        ]
        return custom + urls

    def select_html_view(self, request):
        if request.method == "POST":
            return redirect(
                request.build_absolute_uri(
                    "../create-from-html/map/"
                ) + f"?html_file={request.POST['html_file']}&subject={request.POST['subject']}"
            )
        html_files = sorted(f for f in os.listdir(HTML_TEMPLATES_DIR) if f.endswith(".html"))
        return render(request, "mailing/select-html-template.html", {"html_files": html_files})

    def map_fields_view(self, request):
        html_file = request.POST.get("html_file") or request.GET.get("html_file", "")
        subject = request.POST.get("subject") or request.GET.get("subject", "")

        html_path = os.path.join(HTML_TEMPLATES_DIR, html_file)
        with open(html_path, "r", encoding="utf-8") as f:
            raw_html = f.read()

        substitutions = sorted(extract_substitutions(raw_html))
        cids = sorted(extract_cids(raw_html))
        img_files = sorted(os.listdir(IMG_DIR)) if os.path.isdir(IMG_DIR) else []

        if request.method == "POST":
            sub_map = {var: request.POST[f"sub_{var}"] for var in substitutions}
            img_map = {cid: request.POST[f"cid_{cid}"] for cid in cids if request.POST.get(f"cid_{cid}")}

            from premailer import transform
            light_css = """
            body {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            """

            compiled_body = transform(
                raw_html,
                css_text=light_css
            )

            c_bus.dispatch(CreateTemplateFromHtml(
                subject=subject,
                body=compiled_body,
                substitutions=sub_map,
                images=img_map,
            ))
            self.message_user(request, f"Template '{subject}' created successfully.")
            return redirect("../../../")

        return render(request, "mailing/map-template-fields.html", {
            "html_file": html_file,
            "subject": subject,
            "substitutions": substitutions,
            "cids": cids,
            "contact_fields": CONTACT_FIELDS,
            "img_files": img_files,
        })


@admin.register(MailModel)
class MailAdmin(SummernoteModelAdmin):
    list_display = ["subject", "contact", "status", "send_date"]
    list_filter = ["status"]
    summernote_fields = ['body',]
    actions = ["send_mails"]

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("review/", self.admin_site.admin_view(self.review_mail_view), name="mailing_mail_review"),
        ]
        return custom + urls

    @admin.action(description="Send mails")
    def send_mails(self, request, queryset):
        uuids = list(queryset.values_list("uuid", flat=True))
        request.session["mail_review_queue"] = uuids
        request.session["mail_review_sent"] = 0
        request.session["mail_review_declined"] = 0
        request.session["mail_review_errors"] = 0
        return redirect(reverse("admin:mailing_mail_review"))

    def review_mail_view(self, request):
        queue = request.session.get("mail_review_queue", [])
        changelist_url = reverse("admin:mailing_mailmodel_changelist")

        if not queue:
            self._add_review_summary(request)
            return redirect(changelist_url)

        current_uuid = queue[0]
        mail = get_object_or_404(MailModel, uuid=current_uuid)

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "accept":
                try:
                    c_bus.dispatch(SendMail(mail_id=current_uuid))
                    request.session["mail_review_sent"] = request.session.get("mail_review_sent", 0) + 1
                except Exception as e:
                    request.session["mail_review_errors"] = request.session.get("mail_review_errors", 0) + 1
                    self.message_user(request, f"Error sending to {mail.contact}: {type(e).__name__}: {e}", level="error")
                queue.pop(0)
                request.session["mail_review_queue"] = queue
                request.session.modified = True
                return redirect(reverse("admin:mailing_mail_review"))

            elif action == "decline":
                queue.pop(0)
                request.session["mail_review_queue"] = queue
                request.session["mail_review_declined"] = request.session.get("mail_review_declined", 0) + 1
                request.session.modified = True
                return redirect(reverse("admin:mailing_mail_review"))

            elif action == "modify":
                new_body = request.POST.get("body", mail.body)
                MailModel.objects.filter(uuid=current_uuid).update(body=new_body)
                return redirect(reverse("admin:mailing_mail_review"))

            elif action == "accept_all":
                for uid in list(queue):
                    try:
                        c_bus.dispatch(SendMail(mail_id=uid))
                        request.session["mail_review_sent"] = request.session.get("mail_review_sent", 0) + 1
                    except Exception as e:
                        m = get_object_or_404(MailModel, uuid=uid)
                        request.session["mail_review_errors"] = request.session.get("mail_review_errors", 0) + 1
                        self.message_user(request, f"Error sending to {m.contact}: {type(e).__name__}: {e}", level="error")
                request.session["mail_review_queue"] = []
                request.session.modified = True
                self._add_review_summary(request)
                return redirect(changelist_url)

        rendered_body = render_body_with_inline_images(mail.body, mail.images, IMG_DIR)
        return render(request, "mailing/review-mail.html", {
            "mail": mail,
            "rendered_body": rendered_body,
            "queue_length": len(queue),
        })

    def _add_review_summary(self, request):
        sent = request.session.pop("mail_review_sent", 0)
        declined = request.session.pop("mail_review_declined", 0)
        errors = request.session.pop("mail_review_errors", 0)
        request.session.pop("mail_review_queue", None)
        self.message_user(request, f"Review done: {sent} sent, {declined} declined, {errors} error(s).")

