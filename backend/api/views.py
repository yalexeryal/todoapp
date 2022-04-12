from django.shortcuts import render
from rest_framework import generics, permissions
from .serializerrs import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo
from django.db import InternalError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Пользователь может только обновлять, удалять собственные сообщения"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TodoListCreate(generics.ListCreateAPIView):
    """Только зарегистрированный пользователь может добовлять сообщения"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoToggleComplete(generics.UpdateAPIView):
    """Помечает как завершенный"""
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not (serializer.instance.completed)
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except InternalError:
            return JsonResponse(
                {'error': 'username taken.choose another username'}, status=400
            )


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
    user = authenticate(request, username=data['username'],
                        password=data['password'])
    if user is None:
        return JsonResponse(
            {'error': 'unable to login. check username and password'}, status=400)
    else:  # возвращать токен пользователя
        try:
            token = Token.objects.get(user=user)
        except:  # если токена нет в базе данных, создайте новый токен
            token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=201)
