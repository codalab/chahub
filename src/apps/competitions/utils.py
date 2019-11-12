import requests
import logging

from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile

from competitions.models import Competition

logger = logging.getLogger(__name__)


def competition_download_image(competition_pk):
    try:
        comp = Competition.objects.get(pk=competition_pk)
    except ObjectDoesNotExist:
        logger.warning("Competition not found")
        return
    logger.info("Competition found")
    if comp.logo_url == '/static/img/img-wireframe.png' or '':
        comp.logo_url = None
        comp.save()
        return
    resp = requests.get(comp.logo_url)
    content_type = resp.headers.get('Content-Type', '')
    logger.info(
        "Response; Status: {0}, Content-Type: {1}".format(resp.status_code, content_type.lower())
    )
    # TODO this is only saving PNGs, and isn't actually saving them to the competition.
    # if content_type.lower() == 'image/png':
        logger.info("Image found")
        image = Image.open(BytesIO(resp.content))
        width, height = image.size
        aspect = width / height
        image_format = image.format
        unsimplified_ratio = "{0}/{1}".format(width, height)
        logger.info("Aspect ratio is: {0}, or: {1} unsimplified".format(aspect, unsimplified_ratio))
        new_width = settings.LOGO_BASE_WIDTH
        new_height = int(round(new_width * aspect))
        logger.info("New Width: {0}, New Height: {1}".format(new_width, new_height))
        image_rs = image.resize((new_width, new_height), Image.ANTIALIAS)
        thumb_io = BytesIO()
        image_rs.save(thumb_io, format=image_format)
        new_image = ContentFile(thumb_io.getvalue())
        comp.logo.save('logo_{0}.{1}'.format(comp.pk, image_format.lower()), new_image)
        comp.save()
        logger.info("Image file saved for competition {}".format(comp.pk))
    # else:
    #     logger.warning("Image not found")
