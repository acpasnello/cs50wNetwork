from django.contrib import admin
from .models import Post, Like, Follow, User

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ('pk', 'poster', 'content', 'posted', 'lastmodified', 'likecount')
    readonly_fields = ('pk', 'posted', 'lastmodified')

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(User)
