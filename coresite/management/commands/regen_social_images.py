from django.core.management.base import BaseCommand

from coresite.models import BlogPost
from coresite.services.social_images import generate_social_images


class Command(BaseCommand):
    help = "Regenerate social images for blog posts"

    def add_arguments(self, parser):
        parser.add_argument("--slug", help="Slug of post to regenerate")
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing files even if they exist",
        )

    def handle(self, *args, **options):
        qs = BlogPost.objects.all()
        if options.get("slug"):
            qs = qs.filter(slug=options["slug"])
        for post in qs:
            og_url, twitter_url = generate_social_images(post, force=options.get("force"))
            BlogPost.objects.filter(pk=post.pk).update(
                og_image_url=og_url, twitter_image_url=twitter_url
            )
            self.stdout.write(f"Generated images for {post.slug}")
