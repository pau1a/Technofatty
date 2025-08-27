from django.core.management.base import BaseCommand
from django.utils import timezone
from coresite.models import KnowledgeArticle, StatusChoices


class Command(BaseCommand):
    help = "Publish scheduled knowledge articles whose publish time has arrived"

    def handle(self, *args, **options):
        now = timezone.now()
        articles = KnowledgeArticle.objects.filter(
            status=StatusChoices.DRAFT, published_at__isnull=False, published_at__lte=now
        )
        count = 0
        for article in articles:
            article.status = StatusChoices.PUBLISHED
            article.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Published {count} articles."))
