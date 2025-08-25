from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0006_article_slug_per_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_type", models.CharField(max_length=100)),
                ("meta", models.JSONField(default=dict, blank=True)),
                ("ip_hash", models.CharField(max_length=64, blank=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-timestamp"]},
        ),
    ]
