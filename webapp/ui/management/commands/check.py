from django.core.management.base import BaseCommand, CommandError
from library.ui.models import Media
from settings import MEDIA_ROOT
import os
import urllib
import string

class Command(BaseCommand):
    args = '<location1 location2 ...>'
    help = 'check for errors and inconsistencies'

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
            medias = Media.objects.all().order_by('locationSingularString')

        print 'Check for missing cover art'
        print '---------------------------'
        for media in medias:
            location = media.locationSingularString.strip(string.lowercase)
            name = 'images/scanned/' + location + '_front.jpg'
            path = MEDIA_ROOT + "/" + name
            if not os.path.exists(path):
                print '%s: %s' % (media.locationSingularString, media.title)


        print ' '
        print 'Check Movies with no Media entry'
        print '--------------------------------'

        fix = []
        files = os.listdir(MEDIA_ROOT + '/files')
        for f in files:
            loc = f.split('_')
            try:
                media = Media.objects.get(locationSingularString=loc[0])
            except Media.DoesNotExist:
                print loc[0]
                fix.append(f)

        fix.sort()
        for p in fix:
            print p


