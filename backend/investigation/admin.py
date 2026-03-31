from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from .models import ClueModel, ContactForReviewModel, BlacklistModel
from hex.investigation.app import ApproveContact, RejectContact
from hex.investigation.domain import DuplicateContact
from hex.investigation.infra.buses import i_bus


@admin.register(ClueModel)
class ClueAdmin(admin.ModelAdmin):
    list_display = ["clue_truncated", "status", "type", "score", "times_returned","created_at"]
    list_filter = ["status", "type"]
    search_fields = ["clue"]
    actions = ["mark_blacklisted", "reset_to_pending"]

    def clue_truncated(self, obj):
        return obj.clue[:80]
    clue_truncated.short_description = "Clue"

    @admin.action(description="Mark as blacklisted")
    def mark_blacklisted(self, request, queryset):
        queryset.update(status="blacklisted")

    @admin.action(description="Reset to pending")
    def reset_to_pending(self, request, queryset):
        queryset.update(status="pending")


@admin.register(ContactForReviewModel)
class ContactForReviewAdmin(admin.ModelAdmin):
    list_display = ["nom", "mail", "status", "idioma", "source_clue"]
    list_filter = ["status", "idioma"]
    search_fields = ["nom", "mail"]
    actions = ["review_contacts"]

    @admin.action(description="Review contacts")
    def review_contacts(self, request, queryset):
        uuids = list(queryset.filter(status="pending").values_list("uuid", flat=True))
        request.session["cfr_review_queue"] = uuids
        request.session["cfr_review_approved"] = 0
        request.session["cfr_review_rejected"] = 0
        request.session["cfr_review_skipped"] = 0
        return redirect(reverse("admin:investigation_cfr_review"))

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("review/", self.admin_site.admin_view(self.review_contact_view), name="investigation_cfr_review"),
        ]
        return custom + urls

    def review_contact_view(self, request):
        queue = request.session.get("cfr_review_queue", [])
        changelist_url = reverse("admin:investigation_contactforreviewmodel_changelist")

        if not queue:
            self._add_review_summary(request)
            return redirect(changelist_url)

        current_uuid = queue[0]
        contact = get_object_or_404(ContactForReviewModel, uuid=current_uuid)

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "approve":
                try:
                    i_bus.dispatch(ApproveContact(contact_for_review_uuid=current_uuid))
                    request.session["cfr_review_approved"] = request.session.get("cfr_review_approved", 0) + 1
                except DuplicateContact as e:
                    self.message_user(request, f"Duplicate: {e}", level="error")
                queue.pop(0)
                request.session["cfr_review_queue"] = queue
                request.session.modified = True
                return redirect(reverse("admin:investigation_cfr_review"))

            elif action == "reject":
                i_bus.dispatch(RejectContact(contact_for_review_uuid=current_uuid))
                request.session["cfr_review_rejected"] = request.session.get("cfr_review_rejected", 0) + 1
                queue.pop(0)
                request.session["cfr_review_queue"] = queue
                request.session.modified = True
                return redirect(reverse("admin:investigation_cfr_review"))

            elif action == "reject_blacklist":
                i_bus.dispatch(RejectContact(contact_for_review_uuid=current_uuid, blacklist=True))
                request.session["cfr_review_rejected"] = request.session.get("cfr_review_rejected", 0) + 1
                queue.pop(0)
                request.session["cfr_review_queue"] = queue
                request.session.modified = True
                return redirect(reverse("admin:investigation_cfr_review"))

            elif action == "modify":
                ContactForReviewModel.objects.filter(uuid=current_uuid).update(
                    nom=request.POST.get("nom", contact.nom),
                    mail=request.POST.get("mail", contact.mail),
                    web=request.POST.get("web", contact.web),
                    persona_contacte=request.POST.get("persona_contacte", contact.persona_contacte),
                    telefon=request.POST.get("telefon", contact.telefon),
                    notes=request.POST.get("notes", contact.notes),
                    idioma=request.POST.get("idioma", contact.idioma),
                )
                return redirect(reverse("admin:investigation_cfr_review"))

            elif action == "skip":
                request.session["cfr_review_skipped"] = request.session.get("cfr_review_skipped", 0) + 1
                queue.pop(0)
                request.session["cfr_review_queue"] = queue
                request.session.modified = True
                return redirect(reverse("admin:investigation_cfr_review"))

        return render(request, "investigation/review-contact.html", {
            "contact": contact,
            "queue_length": len(queue),
        })

    def _add_review_summary(self, request):
        approved = request.session.pop("cfr_review_approved", 0)
        rejected = request.session.pop("cfr_review_rejected", 0)
        skipped = request.session.pop("cfr_review_skipped", 0)
        request.session.pop("cfr_review_queue", None)
        self.message_user(request, f"Review done: {approved} approved, {rejected} rejected, {skipped} skipped.")


@admin.register(BlacklistModel)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ["normalized_name", "mail", "created_at"]
    search_fields = ["normalized_name", "mail"]
