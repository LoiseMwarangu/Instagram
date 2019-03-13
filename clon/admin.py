from django.contrib import admin

from .models import Location,tags, Image, Profile


class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Location)
admin.site.register(tags)
admin.site.register(Image, ImageAdmin)
admin.site.register(Profile)
