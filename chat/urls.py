from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('add_chat_user/', Add_chat_user.as_view()),
    path('free_chat_user/', Free_chat_user.as_view()),
    path('create_chat/', Create_chat.as_view()),
    path('delete_chat/', Delete_chat.as_view()),
    path('user_info/<user_id>', User_info.as_view()),
    path('my_user_info/', My_user_info.as_view()),
    path('messages/<chat_id>', MessageList.as_view()),
]
