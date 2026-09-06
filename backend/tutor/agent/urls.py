from django.urls import path

from .views import SubTopicDetailView, TopicDetailView, TopicListView


urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('subtopics/<int:pk>/', SubTopicDetailView.as_view(), name='subtopic-detail'),
]