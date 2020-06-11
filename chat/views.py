from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import User,Chat
from .serializer import UserSerializer,ChatSerializer
from django.http import HttpResponse


class UserView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChatView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self,request):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):

    def get_object(self,name):
        try:
            return User.objects.get(username=name)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,name):
        try:
            user = self.get_object(name)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request,name):
        user = self.get_object(name)
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,name):
        user = self.get_object(name)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""class ChatDetails(APIView):

    def get_object(self,name):
        try:
            return Chat.objects.get(name=name)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,name):
        chat = self.get_object(name)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def put(self,request,name):
        chat = self.get_object(name)
        serializer = ChatSerializer(chat,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,name):
        chat = self.get_object(name)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


