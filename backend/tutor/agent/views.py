from uuid import uuid4

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CodeSnippet, SubTopic, Topic
from .serializers import (
	CodeSnippetSerializer,
	SubTopicSerializer,
	TopicDetailSerializer,
	TopicSerializer,
)
from .utils.agents.ask import TutorGraph
from .utils.agents.quiz import create_quizzes


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


class ChatQueryView(APIView):
	def post(self, request, subtopic_id):
		query = request.data.get('query')
		if not isinstance(query, str) or not query.strip():
			return Response(
				{'query': 'This field is required.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
		thread_id = request.data.get('thread_id') or str(uuid4())
		topic_graph = TutorGraph()
		result = topic_graph.invoke(
			query=query,
			context=subtopic.summary,
			thread_id=thread_id,
		)

		return Response({
			'answer': result['answer'],
			'thread_id': thread_id,
		})


class QuizCreateView(APIView):
	def post(self, request, subtopic_id):
		subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
		quizzes = create_quizzes(subtopic.summary)

		return Response(quizzes.model_dump())