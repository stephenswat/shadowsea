import random
import datetime

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min, Max, Value, BooleanField, Case, When, F, OuterRef, Subquery, DateTimeField
from django.db.models.functions import Coalesce


from forum.models import Thread, Post, ThreadRead


class ForumView(View):
    def get(self, request):
        request.session.flush()
        return render(request, 'forum/terminal.html')


class ThreadListView(View):
    def get(self, request):
        qs = (
            Thread
            .objects
            .annotate(
                earliest_fake=Subquery(
                    Post.objects.filter(thread__id=OuterRef('id')).order_by('created').values('created')[:1]
                ),
                latest_fake=Subquery(
                    Post.objects.filter(thread__id=OuterRef('id')).order_by('-created').values('created')[:1]
                ),
                earliest_real=Subquery(
                    Post.objects.filter(thread__id=OuterRef('id')).order_by('created_real').values('created_real')[:1]
                ),
                latest_real=Subquery(
                    Post.objects.filter(thread__id=OuterRef('id')).order_by('-created_real').values('created_real')[:1]
                ),
            )
        )

        if request.user.is_authenticated:
            qs = (
                qs
                .annotate(
                    last_read=Coalesce(
                        Subquery(ThreadRead.objects.filter(user=request.user, thread__id=OuterRef('id')).values('date')[:1]),
                        Value(datetime.datetime(1970, 1, 1), DateTimeField())
                    )
                )
            )
        else:
            qs = (
                qs
                .annotate(
                    last_read=Value(datetime.datetime(2200, 1, 1), DateTimeField())
                )
            )

        return JsonResponse([
            {
                'id': t.id,
                'poster': t.poster.username,
                'name': t.name,
                'posts': t.post_set.count(),
                'unread': t.last_read < t.latest_real,
                'date': t.earliest_fake,
                'latest': t.latest_fake,
                'last_read': t.last_read,
            }
            for t in qs
        ], safe=False)


class ThreadView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            ThreadRead.objects.update_or_create(thread_id=id, user=request.user)

        return JsonResponse([
            {
                'poster': p.poster.username,
                'text': p.content,
                'date': p.created
            }
            for p in Post.objects.filter(thread__id=id)
        ], safe=False)


class StatusView(View):
    def get(self, request):
        return JsonResponse({
            'username': request.user.username,
            'logged_in': request.user.is_authenticated
        })


class LoginView(View):
    def post(self, request):
        try:
            username, password = request.POST['token'].split('$', maxsplit=1)
            user = authenticate(request, username=username, password=password)
            login(request, user)

            if user is None:
                raise ValueError("No user found.")

            return JsonResponse({
                'success': True
            })
        except:
            return JsonResponse({
                'success': False
            })


class RegisterView(View):
    def post(self, request):
        username, password = request.POST['token'].split('$', maxsplit=1)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'username taken'
            }, status=409)

        user = User.objects.create_user(username, '', password)
        login(request, user)

        return JsonResponse({
            'success': True
        })


class CreateThreadView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request):
        thread = Thread.objects.create(poster=request.user, name=request.POST['title'])
        Post.objects.create(thread=thread, poster=request.user, content=request.POST['content'])

        ThreadRead.objects.update_or_create(thread_id=thread.id, user=request.user)

        return JsonResponse({'thread_id': thread.id})


class CreatePostView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, id):
        post = Post.objects.create(thread_id=id, poster=request.user, content=request.POST['content'])

        ThreadRead.objects.update_or_create(thread_id=id, user=request.user)

        return JsonResponse({})
