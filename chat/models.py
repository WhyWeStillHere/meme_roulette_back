from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    messeger_1_id = models.ForeignKey(User, related_name='chats_1', on_delete=models.CASCADE)
    messeger_2_id = models.ForeignKey(User, related_name='chats_2', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}) {self.messeger_1_id} - {self.messeger_2_id}'


class ChatUser(models.Model):
    user_id = models.OneToOneField(User, related_name='chat_users', on_delete=models.CASCADE)
    is_free = models.BooleanField()

    def __str__(self):
        return f'{self.user_id}) Free: {self.is_free}'

def upload_path(instance, image_name):
    return '/'.join(['chat_images', image_name])

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='messages', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return f'{self.chat_id}) By {self.author}'