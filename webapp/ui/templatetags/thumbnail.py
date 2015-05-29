from django import template
from library.ui.models import Media
from settings import BASE_URL, MEDIA_URL, MEDIA_ROOT
import os
import string

register = template.Library()

@register.filter
def thumbnail(media):
    location = media.locationSingularString.strip(string.lowercase)
    name =  MEDIA_URL + "thumbnails/" + location + ".jpg"
    path = MEDIA_ROOT + name
    if not os.path.exists(path):
    	name =  MEDIA_URL + "dl2/" + media.uuidString + "-256.png"
    	path = MEDIA_ROOT + "/" + name
    	if not os.path.exists(path):
    	    name = MEDIA_URL + "NoFrontCover256.png"

    return BASE_URL + name

