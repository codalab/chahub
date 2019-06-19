from urllib.parse import urlparse

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from producers.models import Producer
from profiles.models import User, AccountMergeRequest


def validate_next_url(next_url):
    valid_producer_domains = [urlparse(producer.url).netloc for producer in Producer.objects.all()]
    parsed_uri = urlparse(next_url)
    if parsed_uri.netloc in valid_producer_domains or settings.VALID_REDIRECT_DOMAINS:
        return True
    else:
        return False

def send_templated_email(template_name, context, **kwargs):
    subject = kwargs.get('subject')
    # message = kwargs.get('message')
    from_email = kwargs.get('from_email')
    recipient_list = kwargs.get('recipient_list')
    fail_silently = kwargs.get('fail_silently')

    if not subject or not recipient_list:
        raise KeyError("Subject and recipient list not in email kwargs!")

    plain_text = get_template('{}.txt'.format(template_name))
    html_code = get_template('{}.html'.format(template_name))

    # context = {}

    # text_content = html_code.render_to_string(context)
    text_content = plain_text.render(context)
    html_content = html_code.render(context)

    print(html_content)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_content
    )
