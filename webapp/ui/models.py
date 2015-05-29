from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
import tagging

class Fileinfo(models.Model):
    id = models.CharField(primary_key=True, null=True, blank=True, max_length=6)
    filename = models.CharField(null=True, blank=True, max_length=1023)
    secs = models.FloatField(blank=True,null=True)

    def __unicode__(self):
        return self.filename

class Media(models.Model):
    actorsCompositeString = models.CharField(max_length=255,blank=True)
    asin = models.CharField(max_length=255,blank=True)
    associatedURL = models.CharField(max_length=255,blank=True)
    audienceRecommendedAgeSingularString = models.CharField(max_length=255,blank=True)
    boxHeightInInches = models.FloatField(blank=True,null=True)
    boxLengthInInches = models.FloatField(blank=True,null=True)
    boxWeightInPounds = models.FloatField(blank=True,null=True)
    boxWidthInInches = models.FloatField(blank=True,null=True)
    cinematographersCompositeString = models.CharField(max_length=255,blank=True)
    countryCode = models.CharField(max_length=255,blank=True)
    creationDate = models.DateTimeField(blank=True,null=True)
    creatorsCompositeString = models.CharField(max_length=255,blank=True)
    currentValue = models.CharField(max_length=255,blank=True)
    deweyDecimal = models.CharField(max_length=255,blank=True)
    ean = models.CharField(max_length=255,blank=True)
    featuresCompositeString = models.CharField(max_length=255,blank=True)
    formatSingularString = models.CharField(max_length=255,blank=True,db_index=True)
    genresCompositeString = models.CharField(max_length=255,blank=True)
    hasExperienced = models.IntegerField(blank=True,null=True)
    isSigned = models.IntegerField(blank=True,null=True)
    isbn = models.CharField(max_length=255,blank=True)
    languagesCompositeString = models.CharField(max_length=255,blank=True)
    lastModificationDate = models.DateTimeField(blank=True,null=True)
    locationSingularString = models.CharField(max_length=255,blank=True,db_index=True)
    maximumPlayers = models.IntegerField(blank=True,null=True)
    minimumPlayers = models.IntegerField(blank=True,null=True)
    minutes = models.IntegerField(blank=True,null=True)
    netRating = models.FloatField(blank=True,null=True)
    notes = models.CharField(max_length=255,blank=True)
    numberInSeries = models.IntegerField(blank=True,null=True)
    numberOfMedia = models.IntegerField(blank=True,null=True)
    pages = models.IntegerField(blank=True,null=True)
    price = models.CharField(max_length=255,blank=True)
    privateCollection = models.IntegerField(blank=True,null=True)
    publishDate = models.DateTimeField(blank=True,null=True)
    publishersCompositeString = models.CharField(max_length=255,blank=True)
    purchaseDate = models.DateTimeField(blank=True,null=True)
    rare = models.IntegerField(blank=True,null=True)
    rating = models.FloatField(blank=True,null=True)
    seriesSingularString = models.CharField(max_length=255,blank=True)
    subtitle = models.CharField(max_length=255,blank=True,db_index=True)
    theatricalDate = models.DateTimeField(blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,db_index=True)
    type = models.CharField(max_length=255,blank=True)
    used = models.IntegerField(blank=True,null=True)
    uuidString = models.CharField(primary_key=True,max_length=40)
    location = models.ForeignKey('Resource', null=True, blank=True)
    tag_string = TagField()

    def __unicode__(self):
        if len(self.subtitle):
            return self.title + ' / ' + self.subtitle
        else:
            return self.title

class Screening(models.Model):
    timestamp = models.DateTimeField(blank=True)
    start = models.FloatField(blank=True)
    stop = models.FloatField(blank=True)
    media = models.ForeignKey(Media)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.media.title + ' (' + self.user.username + '@' + self.timestamp.isoformat(' ') + ': ' + str(self.start) + '-' + str(self.stop) + ' )'

class Clip(models.Model):
    start = models.FloatField()
    stop = models.FloatField()
    media = models.ForeignKey(Media)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.media.title + ' (' + self.user.username + ': ' + str(self.start) + '-' + str(self.stop) + ')'

class Resource(models.Model):
    id = models.TextField(primary_key=True, null=True, blank=True)
    loc_name = models.TextField(blank=True)
    media_type = models.TextField(blank=True)
    copies = models.IntegerField(null=True, blank=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    title1 = models.TextField(blank=True)
    title2 = models.TextField(blank=True)
    title3 = models.TextField(blank=True)
    subject = models.TextField(blank=True)
    author = models.TextField(blank=True)
    owner_u_login = models.TextField(blank=True)
    url = models.TextField(db_column=u'URL', blank=True) # Field name made lowercase.
    audience = models.TextField(blank=True)
    publication_place = models.TextField(blank=True)
    publisher = models.TextField(blank=True)
    publication_date = models.TextField(blank=True)
    duration = models.TextField(blank=True)
    expiration_date = models.TextField(blank=True)
    filecheck = models.TextField(blank=True)
    fs_name = models.TextField(blank=True)
    image_url = models.TextField(db_column=u'image_URL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'resource'

    def __unicode__(self):
        return self.title


try:
    tagging.register(Media)
except tagging.AlreadyRegistered:
    pass
