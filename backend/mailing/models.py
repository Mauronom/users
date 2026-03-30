from django.db import models


class ContactModel(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    nom = models.CharField(max_length=255)
    mail = models.EmailField()
    web = models.CharField(max_length=255, blank=True)
    persona_contacte = models.CharField(max_length=255, blank=True)
    telefon = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    data_enviat = models.DateField(null=True, blank=True)
    idioma = models.CharField(max_length=16, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    relevant = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} <{self.mail}>"

    class Meta:
        app_label = "mailing"


class TemplateModel(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    substitutions = models.JSONField(default=dict, blank=True)
    attachments = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        app_label = "mailing"


class MailModel(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("sent", "Sent"), ("error", "Error")]

    uuid = models.CharField(max_length=64, unique=True)
    send_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    contact = models.ForeignKey(ContactModel, on_delete=models.CASCADE, null=True, blank=True, related_name="mails")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = "mailing"
