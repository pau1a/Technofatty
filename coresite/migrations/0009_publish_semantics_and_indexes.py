from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0008_knowledgearticle_expansion"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="knowledgearticle",
            name="unique_article_slug_per_category",
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="slug",
            field=models.SlugField(
                blank=True,
                unique=True,
                help_text="Unique across all knowledge articles for future routing flexibility",
            ),
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("published", "Published"),
                    ("archived", "Archived"),
                ],
                default="draft",
                max_length=20,
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="published_at",
            field=models.DateTimeField(blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="image_alt",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddIndex(
            model_name="knowledgearticle",
            index=models.Index(
                fields=["status", "published_at"],
                name="knowledgearticle_status_published_at_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="knowledgearticle",
            index=models.Index(
                fields=["category", "status", "published_at"],
                name="knowledgearticle_category_status_published_at_idx",
            ),
        ),
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS coresite_knowledgearticle_tags_tag_id_idx ON coresite_knowledgearticle_tags (knowledgetag_id);",
            reverse_sql="DROP INDEX IF EXISTS coresite_knowledgearticle_tags_tag_id_idx;",
        ),
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS coresite_knowledgearticle_tags_article_id_idx ON coresite_knowledgearticle_tags (knowledgearticle_id);",
            reverse_sql="DROP INDEX IF EXISTS coresite_knowledgearticle_tags_article_id_idx;",
        ),
    ]
