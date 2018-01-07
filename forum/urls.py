from django.urls import path, include
from django.views.generic import TemplateView

import forum.views

urlpatterns = [
    path('', forum.views.ForumView.as_view()),
    path('status/', forum.views.StatusView.as_view()),
    path('thread/list/', forum.views.ThreadListView.as_view()),
    path('thread/post/', forum.views.CreateThreadView.as_view()),
    path('thread/<int:id>/', forum.views.ThreadView.as_view()),
    path('thread/<int:id>/post/', forum.views.CreatePostView.as_view()),
    path('auth/login/', forum.views.LoginView.as_view()),
    path('auth/register/', forum.views.RegisterView.as_view())
]
