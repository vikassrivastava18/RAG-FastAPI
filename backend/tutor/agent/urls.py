from django.urls import path

from .views import SubTopicDetailView, TopicListView


urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('subtopics/<int:pk>/', SubTopicDetailView.as_view(), name='subtopic-detail'),
]