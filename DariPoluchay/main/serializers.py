from rest_framework import serializers
from .models import *

class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'
        depth = 1

class TgUserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class PresentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Present
        fields = '__all__'
        depth = 2

class PresentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Present
        fields = '__all__'


class PassedBoardHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PassedBoardHistory
        fields = '__all__'
        depth = 1

class PassedBoardHistorySerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = PassedBoardHistory
        fields = '__all__'


class RefLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefLinks
        fields = '__all__'
        depth = 1

class RefLinksSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = RefLinks
        fields = '__all__'
