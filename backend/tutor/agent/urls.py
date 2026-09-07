from django.urls import path

from .views import (
    CodeSnippetDetailView,
    SubTopicDetailView,
    TopicDetailView,
    TopicListView,
)

# Topics URL
urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),    
    path('code-snippets/<int:pk>/', CodeSnippetDetailView.as_view(), name='code-snippet-detail'),
]

# Subtopics URL
urlpatterns += [
    path('subtopics/<int:pk>/', SubTopicDetailView.as_view(), name='subtopic-detail'),
]