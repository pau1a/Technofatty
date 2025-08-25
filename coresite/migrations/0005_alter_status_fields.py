from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0004_blogpost_knowledgecategory_knowledgearticle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="knowledgecategory",
            name="status",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("draft", "Draft"),
                    ("review", "Review"),
                    ("published", "Published"),
                ],
                default="draft",
            ),
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="status",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("draft", "Draft"),
                    ("review", "Review"),
                    ("published", "Published"),
                ],
                default="draft",
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="status",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("draft", "Draft"),
                    ("review", "Review"),
                    ("published", "Published"),
                ],
                default="draft",
            ),
        ),
    ]
