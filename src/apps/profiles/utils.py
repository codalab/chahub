from urllib.parse import urlparse

from django.conf import settings

from producers.models import Producer


def validate_next_url(next_url):
    valid_producer_domains = [urlparse(producer.url).netloc for producer in Producer.objects.all()]
    parsed_uri = urlparse(next_url)
    return parsed_uri.netloc in valid_producer_domains or settings.VALID_REDIRECT_DOMAINS
