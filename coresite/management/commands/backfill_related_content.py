from django.core.management.base import BaseCommand
from coresite.models import BlogPost

PLACEHOLDER = "<!-- related-content -->"


class Command(BaseCommand):
    help = "Append related content placeholder to blog posts missing it"

    def handle(self, *args, **options):
        updated = 0
        for post in BlogPost.objects.all():
            if PLACEHOLDER not in post.content:
                post.content = (post.content or "") + f"\n\n{PLACEHOLDER}\n"
                post.save(update_fields=["content"])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} posts"))
