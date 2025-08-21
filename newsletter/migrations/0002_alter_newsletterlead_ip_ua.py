from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsletterlead",
            name="ip",
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="newsletterlead",
            name="ua",
            field=models.TextField(blank=True, null=True),
        ),
    ]

