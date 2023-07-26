from rest_framework import serializers
from .models import *

class AdminTgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTgUser
        fields = '__all__'

class HelpTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpText
        fields = '__all__'

class InlineMurkupButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineMurkupButton
        fields = '__all__'

class InlineKeyboardMurkupButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineKeyboardMurkupButton
        fields = '__all__'

class HelpTextMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpTextMedia
        fields = '__all__'

