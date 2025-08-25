from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0005_alter_status_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="knowledgearticle",
            name="slug",
            field=models.SlugField(),
        ),
        migrations.AddConstraint(
            model_name="knowledgearticle",
            constraint=models.UniqueConstraint(
                fields=("category", "slug"),
                name="unique_article_slug_per_category",
            ),
        ),
    ]
