from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'tgusers', TgUserViewSet)
router.register(r'boards', BoardViewSet)
router.register(r'presents', PresentViewSet)
router.register(r'passedboards', PassedBoardHistoryViewSet)
router.register(r'reflinks', RefLinksViewSet)



urlpatterns = [
    path('', include(router.urls)),
]
