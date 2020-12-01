from django.contrib import admin
from qtfile.models import File
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'date')
admin.site.register(File, FileAdmin)

