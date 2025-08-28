from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coresite", "0009_publish_semantics_and_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tool",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="tools/"
                    ),
                ),
                ("external_url", models.URLField(blank=True)),
                ("schema_kind", models.CharField(blank=True, max_length=100)),
                ("is_published", models.BooleanField(default=False)),
                ("is_premium", models.BooleanField(default=False)),
                ("display_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ("display_order", "title"),
                "indexes": [
                    models.Index(
                        fields=["is_published", "display_order"],
                        name="tool_pub_order_idx",
                    ),
                    models.Index(fields=["schema_kind"], name="tool_schema_idx"),
                ],
            },
        ),
    ]

