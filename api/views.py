from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskSerializer
from base.models import Task

# Create your views here.


class GetTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class PutTask(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class PostTask(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class DeleteTask(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
