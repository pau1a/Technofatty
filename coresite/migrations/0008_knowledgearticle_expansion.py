from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0007_contactevent"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KnowledgeTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="subtype",
            field=models.CharField(blank=True, choices=[
                ("guide", "Guide"),
                ("glossary", "Glossary"),
                ("signal", "Signal"),
                ("quick_win", "Quick Win"),
            ], max_length=20),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="published_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="knowledge_articles",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="reading_time",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="attribution",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="articles", to="coresite.knowledgetag"),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="knowledge/"),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="image_alt",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="motif",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="meta_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="meta_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="canonical_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="og_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="og_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="og_image_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="twitter_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="twitter_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="knowledgearticle",
            name="twitter_image_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="knowledgearticle",
            name="slug",
            field=models.SlugField(blank=True),
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
            ),
        ),
        migrations.AlterField(
            model_name="knowledgecategory",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("published", "Published"),
                    ("archived", "Archived"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("published", "Published"),
                    ("archived", "Archived"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
    ]
