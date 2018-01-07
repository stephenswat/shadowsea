from django.contrib import admin

from forum.models import Thread, Post


class PostInline(admin.TabularInline):
    model = Post
    ordering = ('created',)

class ThreadAdmin(admin.ModelAdmin):
    inlines = (PostInline, )

admin.site.register(Thread, ThreadAdmin)
