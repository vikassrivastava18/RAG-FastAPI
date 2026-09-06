from rest_framework import generics

from .models import CodeSnippet, SubTopic, Topic
from .serializers import (
	CodeSnippetSerializer,
	SubTopicSerializer,
	TopicDetailSerializer,
	TopicSerializer,
)


class TopicListView(generics.ListAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicSerializer


class TopicDetailView(generics.RetrieveAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicDetailSerializer


class SubTopicDetailView(generics.RetrieveAPIView):
	queryset = SubTopic.objects.all()
	serializer_class = SubTopicSerializer


class CodeSnippetDetailView(generics.RetrieveAPIView):
	queryset = CodeSnippet.objects.all()
	serializer_class = CodeSnippetSerializer
