from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.sites.models import Site


def send_templated_email(template_name, context, subject, recipient_list, from_email=None, fail_silently=False):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    try:
        site_domain = Site.objects.get_current().domain
    except Site.DoesNotExist:
        site_domain = 'example.com'
    context["site_domain"] = site_domain
    plain_text = get_template(f'{template_name}.txt')
    html_code = get_template(f'{template_name}.html')

    text_content = plain_text.render(context)
    html_content = html_code.render(context)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_content
    )
