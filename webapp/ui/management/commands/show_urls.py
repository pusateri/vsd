from django.core.management.base import BaseCommand, CommandError
from library.ui.models import Media
from settings import MEDIA_URL
import os
import urllib

class Command(BaseCommand):
    args = '<location1 location2 ...>'
    help = 'show URL locations'

    def handle(self, *args, **options):
        
        medias = []
        if len(args):
            for location in args:
                try:
                    media = Media.objects.get(locationSingularString=location)
		    medias.append(media)
                except Media.DoesNotExist:
                    raise CommandError('Media "%s" does not exist' % location)
        else:
            medias = Media.objects.all()

        for media in medias.order_by('locationSingularString'):
            if media.associatedURL:
                print media.locationSingularString + ";" + media.associatedURL
            else:
                print media.locationSingularString + ";None"
