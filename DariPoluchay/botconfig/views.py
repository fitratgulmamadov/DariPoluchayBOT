from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *



class AdminTgUserViewSet(viewsets.ModelViewSet):
    queryset = AdminTgUser.objects.all()
    serializer_class = AdminTgUserSerializer

class HelpTextViewSet(viewsets.ModelViewSet):
    queryset = HelpText.objects.all()
    serializer_class = HelpTextSerializer
    lookup_field = 'name'

class HelpTextMediaViewSet(viewsets.ModelViewSet):
    queryset = HelpTextMedia.objects.all()
    serializer_class = HelpTextMediaSerializer
    lookup_field = 'name'


class InlineMurkupButtonViewSet(viewsets.ModelViewSet):
    queryset = InlineMurkupButton.objects.all()
    serializer_class = InlineMurkupButtonSerializer

class InlineKeyboardMurkupButtonViewSet(viewsets.ModelViewSet):
    queryset = InlineKeyboardMurkupButton.objects.all()
    serializer_class = InlineKeyboardMurkupButtonSerializer