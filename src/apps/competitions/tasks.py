import logging
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile

from celery_config import app
from competitions.models import Competition

logger = logging.getLogger()


@app.task(queue='site-worker', soft_time_limit=60)
def download_competition_image(comp_pk):
    try:
        comp = Competition.objects.get(id=comp_pk)
    except Competition.DoesNotExist:
        logger.warning('Could not find competition')
        return

    if comp.logo_url == '/static/img/img-wireframe.png' or '':
        comp.logo_url = None
        comp.save()
        return
    resp = requests.get(comp.logo_url)
    content_type = resp.headers.get('Content-Type', '')
    logger.info(
        f"Response - Status: {resp.status_code}, Content-Type: {content_type.lower()}"
    )
    if content_type.lower().startswith('image/'):
        logger.info("Image found")
        image = Image.open(BytesIO(resp.content))
        width, height = image.size
        aspect = width / height
        image_format = image.format
        logger.info(f"Aspect ratio is: {aspect}, or: {width}/{height} unsimplified")
        new_width = settings.LOGO_BASE_WIDTH
        new_height = int(round(new_width / aspect))
        logger.info(f"New Width: {new_width}, New Height: {new_height}")
        image_rs = image.resize((new_width, new_height), Image.ANTIALIAS)
        thumb_io = BytesIO()
        image_rs.save(thumb_io, format=image_format)
        new_image = ContentFile(thumb_io.getvalue())
        comp.logo.save(f'logo_{comp.pk}.{image_format.lower()}', new_image)
        comp.save()
        logger.info(f"Image file saved for competition {comp.pk}")
    else:
        logger.warning("Image not found")
