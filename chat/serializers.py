from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'messeger_1_id']

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = '__all__'
    
class MessageSerializerGet(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['chat_id', 'author', 'image_url']

    def get_image_url(self, post):
        try:
            image_url = post.image.url
            request = self.context['request']
            return request.build_absolute_uri(image_url)
        except Exception:
            return None

class MessageSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']