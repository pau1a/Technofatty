from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0012_alpha_beta_case_studies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="meta_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="meta_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="canonical_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="og_image_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="twitter_image_url",
            field=models.URLField(blank=True),
        ),
    ]
