from django.urls import path
from .views import (PostListView, PostCreateView, PostDetailView, ResponsesView, PostEditView,
                    confirm_comment, delete_comment)

urlpatterns = [
     path("", PostListView.as_view(), name='post_list'),
     path("post/create/", PostCreateView.as_view(), name='post_create'),
     path("post/<int:pk>/edit/", PostEditView.as_view(), name='post_edit'),
     path("post/<int:pk>/", PostDetailView.as_view(), name='post_detail'),
     path("responses/", ResponsesView.as_view(), name="responses"),
     path('response/<int:resp_id>/confirm/', confirm_comment, name='confirm_comment'),
     path('response/<int:resp_id>/delete/', delete_comment, name='delete_comment'),
]