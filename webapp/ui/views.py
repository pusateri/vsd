from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.utils.simplejson import loads
from django.contrib.auth.models import User
from django.db.models import Q
from tagging.models import Tag, TaggedItem
from settings import BASE_URL, BASE_URL_NO_SSL, MEDIA_URL, MEDIA_ROOT
from urlparse import urlparse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from library.ui.models import Media, Resource, Screening, Fileinfo
from operator import itemgetter
import os
import re
import string
import dateutil.parser

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@login_required
def search(request):
    query_string = ''
    movie_list = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'subtitle', 'location__description', 'location__subject',])

        movie_list = Media.objects.filter(entry_query).order_by('title')

    if len(query_string) == 0:
        movie_list = Media.objects.all().order_by('title')

    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'

    return render_to_response('ui/list.html',
                              {'movie_list': movie_list, 'media_url': MEDIA_URL, 'sort_key':'title', 'user':local_user, 'query_string':query_string})

def sortby(request):
    movie_list = None
    sort_key = 'title'
    if ('key' in request.GET) and request.GET['key'].strip():
        sort_key = request.GET['key']
        movie_list = Media.objects.all().order_by(sort_key, 'title')

    return render_to_response('ui/index.html', {
        'movie_list': movie_list,
        'media_url': MEDIA_URL,
        'sort_key': sort_key,
    })

@csrf_exempt
def transport(request):
    if request.method != 'POST':
        return HttpResponse("Error: POST expected")
    json_string = request.POST.get('json', False)
    if json_string is None:
        return HttpResponse("Error: JSON expected")
    data = loads(json_string)
    timestamp = None
    time_string = data.get('timestamp')
    if time_string:
        timestamp = dateutil.parser.parse(time_string)
    if timestamp is None:
        return HttpResponse("Error: bad timestamp")
    name = data.get('user')
    if name is None:
        return HttpResponse("Error: bad user")
    uid = data.get('media')
    if uid is None:
        return HttpResponse("Error: bad media")
    start = data.get('start')
    stop = data.get('stop')
    if stop > 0:
        # update screening instance
        s = Screening.objects.get(timestamp=timestamp, media__uuidString=uid, user__username=name)
        s.stop = stop
    else:
        # create screening instance
        s = Screening()
        s.timestamp = timestamp
        s.media = Media.objects.get(uuidString=uid)
        s.user = User.objects.get(username=name)
        s.start = start
        s.stop = 0
    s.save()
    return HttpResponse("OK")


@login_required
def top_tags(request):
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    # look up what the user has been playing recently
    medias = Screening.objects.filter(user__username=local_user).order_by('-timestamp').values_list('media', flat=True).distinct()[:30]
    recent = Media.objects.filter(uuidString__in=[str(m) for m in medias])

    # figure out the most common tags
    tag_count = {}
    for p in recent:
        tags = Tag.objects.get_for_object(p)
        if len(tags):
            for t in tags:
                count = tag_count.get(t.name)
                if count is None:
                    tag_count[t.name] = 1
                else:
                    tag_count[t.name] = count + 1

    default_tags = ['animated', 'biology', 'history', 'literature', 'science']

    tag_list = sorted(tag_count.iteritems(), key=itemgetter(1), reverse=True)
    pool = []
    tag_dict = {}
    for tag_name, count in tag_list[:30]:
        tag_object = Tag.objects.get(name=tag_name)
        entries = TaggedItem.objects.get_by_model(Media, tag_object).order_by('?')[:4]
        if len(entries) > 3:
            pool.append(tag_name)
            tag_dict[tag_name] = entries

    j = 0
    count = len(tag_dict)
    if count < 5:
        for i in range(count, 5):
            tag_name = default_tags[j]
            if not tag_name in pool:
                tag_object = Tag.objects.get(name=tag_name)
                entries = TaggedItem.objects.get_by_model(Media, tag_object).order_by('?')[:4]
                tag_dict[tag_name] = entries
            j = j + 1

    return render_to_response('ui/top_tags.html', dict(tag_dict=tag_dict, user=local_user, media_url=MEDIA_URL, recent=recent[:4], next='/'))

@login_required
def with_tag(request, tag, object_id=None, page=1):
    tag = tag.replace('-', ' ')
    query_tag = Tag.objects.get(name=tag)
    entries = TaggedItem.objects.get_by_model(Media, query_tag)
    entries = entries.order_by('title')
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    return render_to_response('ui/with_tag.html', dict(tag=tag, entries=entries, media_url=MEDIA_URL, user=local_user))

@login_required
def screenings(request):
    screenings = Screening.objects.all().order_by('-timestamp')

    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    return render_to_response('ui/screenings.html', {
            'user':local_user,
            'media_url':MEDIA_URL,
            'screenings':screenings,
            })

def index(request):
    movie_list = Media.objects.all().order_by('title')
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    
    return render_to_response('ui/index.html',
                              {'movie_list': movie_list, 'media_url': MEDIA_URL, 'sort_key':'title', 'user' : local_user})


@login_required
def list(request):
    movie_list = Media.objects.all().order_by('title')
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    
    return render_to_response('ui/list.html',
                              {'movie_list': movie_list, 'media_url': MEDIA_URL, 'sort_key':'title', 'user' : local_user})

@login_required
def location(request):
    movie_list = Media.objects.all().order_by('locationSingularString')
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    
    return render_to_response('ui/location.html',
                              {'movie_list': movie_list, 'media_url': MEDIA_URL, 'sort_key':'title', 'user' : local_user})

@login_required
def edittags(request, media_locationSingularString):
    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'
    p = get_object_or_404(Media, locationSingularString=media_locationSingularString)
    taglist = Tag.objects.get_for_object(p)
    alltags = Tag.objects.all()
    return render_to_response('ui/edittags.html', {
            'media':p,
            'media_url':MEDIA_URL,
            'user':local_user,
            'taglist':taglist,
            'alltags':alltags
            })

@csrf_exempt
@login_required
def detail(request, media_locationSingularString):
    image = ''
    image_back = ''
    p = get_object_or_404(Media, locationSingularString=media_locationSingularString)

    if request.user.is_authenticated():
        local_user = request.user.username
    else:
        local_user = 'foo'

    # see if we have a scanned image
    location = p.locationSingularString.strip(string.lowercase)
    name = MEDIA_URL + '1440/' + location + '_front.jpg'
    path = MEDIA_ROOT + name
    if os.path.exists(path):
        image = name
        name = MEDIA_URL + '1440/' + location + '_back.jpg'
        path = MEDIA_ROOT + name
        if os.path.exists(path):
            image_back = name

    # otherwise, see if we have a cached image from amazon
    if not len(image):
        if p:
            if len(p.locationSingularString):
                name = 'amazon/' + p.locationSingularString + '.jpg'
                path = MEDIA_ROOT + name
                if os.path.exists(path):
                    image = name

    # if no full size image, use the thumbnail
    if not len(image):
        name = 'dl2/' + p.uuidString + '-256.png'
        path = MEDIA_ROOT + name
        if os.path.exists(path):
            image = name

    if not len(image):
        image = MEDIA_URL + 'NoFrontCover.png'

    locations = []
    num = p.locationSingularString.count(',')
    if num:
        locations = p.locationSingularString.split(',')

    relative = 'playlists/%s/prog_index.m3u8' % p.locationSingularString
    path = MEDIA_ROOT + "/" + relative
    if os.path.exists(path):
        url = BASE_URL_NO_SSL + relative
    else:
        url = ''

    fields = []
    if len(locations):
        loc = locations[0]
    else:
        loc = p.locationSingularString

    try:
        newloc = loc.rstrip(string.ascii_lowercase)
        resource = Resource.objects.get(id=newloc)
        if resource.subject:
            fields.append(('Subject', resource.subject))
        if resource.description:
            fields.append(('Description', resource.description))
    except Resource.DoesNotExist:
        pass

    try:
        finfo = Fileinfo.objects.get(id=loc)
        relative = 'files/%s' % finfo.filename
        path = MEDIA_ROOT + '/' + relative
        if os.path.exists(path):
            file_url = BASE_URL_NO_SSL + relative
        else:
            file_url = ''
    except Fileinfo.DoesNotExist:
        file_url = ''

    tags = Tag.objects.get_for_object(p)

    if len(p.audienceRecommendedAgeSingularString):
        fields.append(('Recommended Age', p.audienceRecommendedAgeSingularString))
    if p.minutes:
        fields.append(('Length', str(p.minutes) + ' minutes'))
    if p.hasExperienced:
        fields.append(('Play Count', p.hasExperienced))
    if len(p.genresCompositeString):
        fields.append(('Genres', p.genresCompositeString))
    if len(p.publishersCompositeString):
        fields.append(('Publishers', p.publishersCompositeString))
    if len(p.actorsCompositeString):
        fields.append(('Actors', p.actorsCompositeString))
    if len(p.cinematographersCompositeString):
        fields.append(('Cinematographers', p.cinematographersCompositeString))
    if len(p.creatorsCompositeString):
        fields.append(('Creators', p.creatorsCompositeString))
    if len(p.featuresCompositeString):
        fields.append(('Features', p.featuresCompositeString))
    if len(p.formatSingularString):
        fields.append(('Format', p.formatSingularString))
    if len(p.languagesCompositeString):
        fields.append(('Languages', p.languagesCompositeString))
    if p.netRating > 0:
        fields.append(('Internet Rating', p.netRating))
    if p.numberInSeries:
        fields.append(('Number in Series', p.numberInSeries))
    if p.rating > 0:
        fields.append(('Rating', p.rating))
    if len(p.seriesSingularString):
        fields.append(('Series', p.seriesSingularString))
    if len(p.type):
        fields.append(('Type', p.type))
    if p.theatricalDate:
        fields.append(('Theatrical Date', p.theatricalDate.strftime("%B %Y")))
    if p.publishDate:
        fields.append(('Published', p.publishDate.strftime("%B %Y")))
    if p.creationDate:
        fields.append(('Added', p.creationDate.strftime("%B %Y")))
    if p.lastModificationDate:
        fields.append(('Entry Modified', p.lastModificationDate.strftime("%B %Y")))
    if len(p.locationSingularString):
        fields.append(('Shelf Location', p.locationSingularString))

    if len(image):
        image = BASE_URL + image
    if len(image_back):
        image_back = BASE_URL + image_back

    screenings = Screening.objects.filter(media__uuidString=p.uuidString).order_by('-timestamp')[:25]

    return render_to_response('ui/detail.html', {
            'media':p,
            'media_url':MEDIA_URL,
            'image':image,
            'image_back':image_back,
            'url':url,
            'file_url':file_url,
            'fields':fields,
            'user':local_user,
            'tags':tags,
            'screenings':screenings,
            })
