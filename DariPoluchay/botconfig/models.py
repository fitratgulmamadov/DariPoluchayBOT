from django.db import models


class AdminTgUser(models.Model):
    name = models.CharField(max_length=150)
    chat_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name



class HelpText(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    text = models.TextField()

    def __str__(self) -> str:
        return self.name

class HelpTextMedia(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    text = models.TextField()
    img = models.ImageField(upload_to='boards/%Y/%m/%d/')

    def __str__(self) -> str:
        return self.name

class InlineMurkupButton(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    callback = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.name

class InlineKeyboardMurkupButton(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    text = models.CharField(max_length=40)    

    def __str__(self) -> str:
        return self.name
