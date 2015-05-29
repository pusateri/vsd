from django.conf.urls.defaults import *
from library.ui import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^library/', include('library.foo.urls')),

    (r'^$', 'library.ui.views.top_tags'),
    (r'^tag/([-_A-Za-z0-9]+)/$','library.ui.views.with_tag'),
    (r'^tag/([-_A-Za-z0-9]+)/page/(d+)/$', 'library.ui.views.with_tag'),
    (r'^screenings/$', views.screenings),
    (r'^list/$', views.list),
    (r'^location/$', views.location),
    (r'^transport/$', views.transport),
    (r'^movies/(?P<media_locationSingularString>[\w,]+)/$', 'library.ui.views.detail'),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'images'}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^edittags/(?P<media_locationSingularString>[\w,]+)/$', views.edittags),

    (r'^search/$', views.search),
    (r'^sortby/$', views.sortby),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
