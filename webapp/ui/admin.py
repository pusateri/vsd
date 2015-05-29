from library.ui.models import Media, Resource, Fileinfo, Screening
from django.contrib import admin

class ResourceAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ('id', 'title', 'duration')
    search_fields = ('id', 'title', 'subject', 'description')

class MediaAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ('locationSingularString', 'title', 'subtitle', 'minutes')
    search_fields = ('locationSingularString', 'title', 'subtitle')

class FileinfoAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ('id', 'secs', 'filename')
    search_fields = ('filename',)

class ScreeningAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ('timestamp', 'user', 'media')
    search_fields = ('user__username', 'media__title', 'media__subtitle', 'media__locationSingularString')

admin.site.register(Resource, ResourceAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Fileinfo, FileinfoAdmin)
admin.site.register(Screening, ScreeningAdmin)
