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

    class Meta:
        app_label = "mailing"


class TemplateModel(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    substitutions = models.JSONField(default=dict)
    attachments = models.JSONField(default=list)
    images = models.JSONField(default=dict)

    class Meta:
        app_label = "mailing"


class MailModel(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("sent", "Sent"), ("error", "Error")]

    uuid = models.CharField(max_length=64, unique=True)
    send_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.JSONField(default=list)
    images = models.JSONField(default=dict)

    class Meta:
        app_label = "mailing"
