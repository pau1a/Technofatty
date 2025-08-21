from django.db import models


class NewsletterLead(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    ua = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.email
