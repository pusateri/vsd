from django.core.management.base import BaseCommand, CommandError
from library.ui.models import Media, Resource
import plistlib
import datetime
import sys
import string
from ui.models import Media

class Command(BaseCommand):
    args = '<Delicious Library 2 plist XML export file'
    help = 'load export file from Delicious Library 2'

    def handle(self, *args, **options):
        
        plist = []
        if not len(args):
            raise CommandError('please specify an XML plist file from DL2')

        for plist_file in args:
            try:
                plist = plistlib.readPlist(plist_file)
            except:
                raise CommandError('plist file "%s" does not exist' % plist_file)

            count = 0
            modified = 0
            for p in plist:
                save = False
                new = False
                location = p.get('locationSingularString')
                if location is None:
                    print "No location for: %s (%s)" % (p.title, p.uuidString)
                    continue
                try:
                    media = Media.objects.get(locationSingularString=location)

                except Media.DoesNotExist:
                    media = Media()
                    save = True
                    new = True

                for key, value in p.iteritems():
                    old = getattr(media, key, None)
                    if new or cmp(old, value) != 0:
                        if not new and key == 'uuidString':
                            print "uuidString doesn't match location"
                            print location, media
                            break

                        if key == 'minutes':
                            continue

#                        print key.encode('ascii', 'ignore') + ': ' + value.encode('ascii', 'ignore') + ' (was: ' + old.encode('ascii', 'ignore') + ')'
                        setattr(media, key, value)
                        if key == 'locationSingularString':
                            loc = value.rstrip(string.ascii_lowercase)
                            try:
                                resource = Resource.objects.get(id=loc)
                                setattr(media, 'location', resource)
                            except Resource.DoesNotExist:
                                pass
                        save = True

                if save:
                    media.save()
                    modified = modified + 1
                count = count + 1

        print 'XML file imported (%d out of %d modified)' % (modified, count)

