from django.db import migrations
from django.utils import timezone


def create_case_studies(apps, schema_editor):
    CaseStudy = apps.get_model('coresite', 'CaseStudy')

    alpha, _ = CaseStudy.objects.update_or_create(
        slug="alpha",
        defaults=dict(
            title="Alpha",
            summary="Alpha Corp improved onboarding with automated workflows.",
            body="Detailed look at Alpha's automation journey.",
            image="case_studies/alpha.png",
            is_published=True,
            display_order=1,
        ),
    )

    beta, _ = CaseStudy.objects.update_or_create(
        slug="beta",
        defaults=dict(
            title="Beta",
            summary="Beta Ltd cut costs 40% using intelligent forecasting.",
            body="Detailed look at Beta's forecasting tools.",
            image="case_studies/beta.png",
            is_published=True,
            display_order=2,
        ),
    )

    CaseStudy.objects.filter(pk=alpha.pk).update(
        updated_at=timezone.datetime(2024, 4, 10, tzinfo=timezone.utc)
    )
    CaseStudy.objects.filter(pk=beta.pk).update(
        updated_at=timezone.datetime(2024, 5, 20, tzinfo=timezone.utc)
    )


def remove_case_studies(apps, schema_editor):
    CaseStudy = apps.get_model('coresite', 'CaseStudy')
    CaseStudy.objects.filter(slug__in=["alpha", "beta"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("coresite", "0011_casestudy"),
    ]

    operations = [
        migrations.RunPython(create_case_studies, remove_case_studies),
    ]
