from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ClueModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("clue", models.TextField(unique=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("investigating", "Investigating"), ("done", "Done"), ("error", "Error"), ("blacklisted", "Blacklisted")], default="pending", max_length=16)),
                ("type", models.CharField(choices=[("scout", "Scout"), ("entity", "Entity"), ("unknown", "Unknown")], default="unknown", max_length=16)),
                ("score", models.IntegerField(default=5)),
                ("source_clue_text", models.TextField(blank=True, default="")),
                ("times_returned", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"app_label": "investigation", "ordering": ["-score", "-times_returned"]},
        ),
        migrations.CreateModel(
            name="ContactForReviewModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.CharField(max_length=64, unique=True)),
                ("nom", models.CharField(max_length=255)),
                ("mail", models.EmailField(unique=True)),
                ("web", models.CharField(blank=True, max_length=255)),
                ("persona_contacte", models.CharField(blank=True, max_length=255)),
                ("telefon", models.CharField(blank=True, max_length=64)),
                ("notes", models.TextField(blank=True)),
                ("idioma", models.CharField(blank=True, max_length=16)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("source_clue", models.CharField(blank=True, max_length=512)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected"), ("duplicate", "Duplicate")], default="pending", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"app_label": "investigation", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="BlacklistModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("normalized_name", models.CharField(blank=True, max_length=255)),
                ("mail", models.EmailField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"app_label": "investigation"},
        ),
    ]
