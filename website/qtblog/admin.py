from django.contrib import admin
from qtblog.models import Tag
from qtblog.models import Blog
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title', 'path', 'date', 'modify', 'state')
    list_display = ('title', 'path', 'date', 'modify', 'state')

class TagAdmin(admin.ModelAdmin):
    list_display = ('value',)
    
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
# Register your models here.
