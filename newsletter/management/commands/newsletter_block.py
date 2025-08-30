from django.core.management.base import BaseCommand, CommandError

from coresite.models import BlogPost
from newsletter.utils import render_block


class Command(BaseCommand):
    help = "Output newsletter block HTML for given blog post slugs"

    def add_arguments(self, parser):
        parser.add_argument("slugs", nargs="+", help="Blog post slugs")

    def handle(self, *args, **options):
        slugs = options["slugs"]
        for i, slug in enumerate(slugs):
            try:
                post = BlogPost.objects.get(slug=slug)
            except BlogPost.DoesNotExist as exc:  # pragma: no cover - user input
                raise CommandError(f"BlogPost with slug '{slug}' does not exist") from exc

            html = render_block(post)
            self.stdout.write(html)
            if i < len(slugs) - 1:
                self.stdout.write("")
