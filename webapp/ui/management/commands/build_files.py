from django.core.management.base import BaseCommand, CommandError
from library.ui.models import Fileinfo, Media
from settings import MEDIA_ROOT
import os
from mutagen.mp4 import MP4

class Command(BaseCommand):
    args = ''
    help = 'build list of media filenames'

    def handle(self, *args, **options):
        files = os.listdir(MEDIA_ROOT + '/files')
        for f in files:
            save = False
            loc = f.split('_')
            if len(loc[0]) > 5 or len(loc[0]) < 1:
                continue
            basename, extension = os.path.splitext(f)
            if not extension in ['.m4v', '.mp4', '.mov']:
                print extension
                continue
            try:
                finfo = Fileinfo.objects.get(id=loc[0])
                if finfo.filename != f:
                    finfo.filename = f
                    save = True
            except Fileinfo.DoesNotExist:
                finfo = Fileinfo(id=loc[0], filename=f)
                save = True

	    try:
		video = MP4(MEDIA_ROOT + '/files/' + f)
	    except:
		print "error: %s" % f
		assert(0)

            secs = round(video.info.length)
	    try:
		media = Media.objects.get(locationSingularString=loc[0])
		minutes = round(secs/60.0)
		if media.minutes != minutes:
		    media.minutes = int(minutes)
		    media.save()
	    except Media.DoesNotExist:
		pass

	    if finfo.secs != secs:
		finfo.secs = secs
		save = True

            if save:
                print 'updating %s (%6.1f): %s' % (loc[0], secs, f)
                finfo.save()
