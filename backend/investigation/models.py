from django.db import models


class ClueModel(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("investigating", "Investigating"),
        ("done", "Done"),
        ("error", "Error"),
        ("blacklisted", "Blacklisted"),
    ]
    TYPE = [
        ("scout", "Scout"),
        ("entity", "Entity"),
        ("unknown", "Unknown"),
    ]
    clue = models.TextField(unique=True)
    status = models.CharField(max_length=16, choices=STATUS, default="pending")
    type = models.CharField(max_length=16, choices=TYPE, default="scout")
    score = models.IntegerField(default=10)
    summary = models.TextField(blank=True, default="")
    web = models.CharField(max_length=512, blank=True, default="")
    source_clue_text = models.TextField(blank=True, default="")
    times_returned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "investigation"
        ordering = ["-score", "-times_returned"]

    def __str__(self):
        return self.clue[:80]


class ContactForReviewModel(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("duplicate", "Duplicate"),
    ]
    uuid = models.CharField(max_length=64, unique=True)
    nom = models.CharField(max_length=255)
    mail = models.EmailField(unique=True)
    web = models.CharField(max_length=255, blank=True)
    persona_contacte = models.CharField(max_length=255, blank=True)
    telefon = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    idioma = models.CharField(max_length=16, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    source_clue = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=16, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "investigation"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nom} <{self.mail}>"


class BlacklistModel(models.Model):
    normalized_name = models.CharField(max_length=255, blank=True)
    mail = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "investigation"

    def __str__(self):
        return self.normalized_name or self.mail
