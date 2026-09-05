from rest_framework import generics

from .models import SubTopic, Topic
from .serializers import SubTopicSerializer, TopicSerializer


class TopicListView(generics.ListAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicSerializer


class SubTopicDetailView(generics.RetrieveAPIView):
	queryset = SubTopic.objects.all()
	serializer_class = SubTopicSerializer
