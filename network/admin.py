from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ('poster', 'content', 'posted', 'lastmodified', 'likecount')
    readonly_fields = ('posted', 'lastmodified')

admin.site.register(Post, PostAdmin)
