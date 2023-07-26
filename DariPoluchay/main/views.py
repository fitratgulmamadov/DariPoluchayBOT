from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS

class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all().order_by('join_date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['board__name', 'status']
    lookup_field = 'ch_id'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TgUserSerializer
        return TgUserSerializerCreate


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('-state')
    serializer_class = BoardSerializer
    lookup_field = 'name'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state']



class PresentViewSet(viewsets.ModelViewSet):
    queryset = Present.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['from_user__ch_id', 'to_user__ch_id', 'status', 'board__id']
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PresentSerializer
        return PresentSerializerCreate


class PassedBoardHistoryViewSet(viewsets.ModelViewSet):
    queryset = PassedBoardHistory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tguser__ch_id', ]
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PassedBoardHistorySerializer
        return PassedBoardHistorySerializerCreate


class RefLinksViewSet(viewsets.ModelViewSet):
    queryset = RefLinks.objects.all()
    lookup_field = 'tguser__ch_id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url', ]
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RefLinksSerializer
        return RefLinksSerializerCreate