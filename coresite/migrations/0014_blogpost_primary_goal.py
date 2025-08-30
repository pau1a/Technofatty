from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0013_blogpost_meta_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="primary_goal",
            field=models.CharField(
                choices=[("newsletter", "Newsletter sign-up"), ("none", "None")],
                default="newsletter",
                max_length=50,
            ),
        ),
    ]
