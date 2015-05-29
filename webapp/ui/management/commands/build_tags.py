from django.core.management.base import BaseCommand, CommandError
from django.db import models
from library.ui.models import Media, Resource
from settings import MEDIA_URL
import os
import urllib
import string
from tagging.models import Tag


class Command(BaseCommand):
    args = '<location1 location2 ...>'
    help = 'extract tags from Resource subject line'

    def handle(self, *args, **options):

        medias = []
        tag_dict = {}
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
            try:
                newloc = media.locationSingularString.rstrip(string.ascii_lowercase)
                resource = Resource.objects.get(id=newloc)
                if resource.subject:
                    keywords = resource.subject.split('/')
                    for bigkey in keywords:
                        morekeys = bigkey.split(';')
                        for akey in morekeys:
                            somekeys = akey.split(',')
                            for akey2 in somekeys:
                                somemorekeys = akey2.split('&')
                                for key in somemorekeys:
                                    key = key.strip().rstrip(':').replace('.', '').lower()
                                    if len(key):
                                        if not tag_dict.has_key(key):
                                            tag_dict[key] = [];
                                        tag_dict[key].append(media.locationSingularString)
            except Resource.DoesNotExist:
                pass

        for key in tag_dict.iterkeys():
            for location in tag_dict[key]:
                media = Media.objects.get(locationSingularString=location)
                Tag.objects.add_tag(media, '"' + key.replace('-', ' ') + '"')

