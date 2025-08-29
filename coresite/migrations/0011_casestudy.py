from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coresite", "0010_tool"),
    ]

    operations = [
        migrations.CreateModel(
            name="CaseStudy",
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
                ("summary", models.TextField(blank=True)),
                ("body", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="case_studies/"
                    ),
                ),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ("display_order", "title"),
                "indexes": [
                    models.Index(
                        fields=["is_published", "display_order"],
                        name="casestudy_pub_order_idx",
                    )
                ],
            },
        ),
    ]

