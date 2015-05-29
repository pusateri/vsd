from django.core.management.base import BaseCommand, CommandError
from library.ui.models import Media
from settings import MEDIA_URL
import os
import urllib

class Command(BaseCommand):
    args = '<location1 location2 ...>'
    help = 'fetch one or more cover art images from amazon'

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

        for media in medias:
	   if len(media.asin):
		name = media.locationSingularString + '.jpg'
		remote = media.asin + '.01._SCLZZZZZZZ_.jpg'
		path = os.getcwd() + MEDIA_URL + 'amazon/' + name
		old = os.getcwd() + MEDIA_URL + 'amazon/' + remote
		if not os.path.exists(path):
                    if os.path.exists(old):
                        print 'moving %s -> %s' % (old, path)
                        os.rename(old, path)
                        continue

		    url = 'http://images.amazon.com/images/P/' + remote
		    print 'fetching "%s"\n' % url
		    fn, info = urllib.urlretrieve(url, path)
		    for key, value in info.items():
			if key == 'content-type' and value == 'image/gif':
			    os.unlink(path)
