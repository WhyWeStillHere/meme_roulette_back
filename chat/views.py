from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import *
from django.contrib.auth.models import User
from .serializers import *

import logging

class Add_chat_user(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        is_free = request.data.get('is_free')
        ChatUser(user_id=user, is_free=is_free).save()
        return HttpResponse(status=200)

class Free_chat_user(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        chat_user = ChatUser.objects.get(user_id=user)
        chat_user.is_free = True
        chat_user.save()
        return HttpResponse(status=200)

class Create_chat(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_1_id = request.user.id
        user_1 = User.objects.get(id=user_1_id)
        chat = None
        if ChatUser.objects.filter(user_id=user_1, is_free=True).count() == 0:
            logging.warning("No user")
            chat = Chat.objects.filter(Q(messeger_2_id=user_1) | Q(messeger_1_id=user_1))
        else:
            chat_user_1 = ChatUser.objects.get(user_id=user_1)
            chat_user_2_set = ChatUser.objects.filter(~Q(user_id=user_1), is_free=True)
            if (chat_user_2_set.count() == 0):
                chat_user_1.is_free = True
                chat_user_1.save()
                logging.warning("No chat")
            else:
                chat_user_2 = chat_user_2_set.first()
                user_2 = getattr(chat_user_2, 'user_id')
                chat_user_1.is_free = False
                chat_user_2.is_free = False
                chat_user_1.save()
                chat_user_2.save()
                Chat(messeger_1_id=user_1, messeger_2_id=user_2).save()

                chat = Chat.objects.filter(messeger_1_id=user_1)
                logging.warning("Creating new chat")

        if chat is None or chat.count() == 0:
            return HttpResponse(status=400)
        else:
            chat = chat.first()
            if getattr(chat.messeger_1_id, 'id') == user_1_id:
                chat.messeger_1_id = chat.messeger_2_id
            serializer = ChatSerializer(chat,
                                        context={"request": request})
            return Response(serializer.data)

class Delete_chat(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_1_id = request.user.id
        user_1 = User.objects.get(id=user_1_id)
        Chat.objects.filter(Q(messeger_2_id=user_1) | Q(messeger_1_id=user_1)).delete()

        return HttpResponse(status=200)

class User_info(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        if user_id == 0:
            user_id = request.user.id
        
        users = User.objects.get(id=user_id)

        serializer = UserSerializerGet(users,
                                       context={"request": request})
        return Response(serializer.data)

class My_user_info(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        
        users = User.objects.get(id=user_id)

        serializer = UserSerializerGet(users,
                                       context={"request": request})
        return Response(serializer.data)


class MessageList(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, chat_id):
        if Chat.objects.filter(id=chat_id).count() == 0:
            return HttpResponse(status=400)
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializerGet(messages,
                                          many=True,
                                          context={"request": request})
        return Response(serializer.data)

    def post(self, request, chat_id):
        logging.warning(request.FILES)
        logging.warning(request.FILES.get('image'))
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=request.user.id)
        message = Message(chat_id=chat, author=user, image=request.FILES.get('image'))
        message.save()
        return self.get(request, chat_id)

