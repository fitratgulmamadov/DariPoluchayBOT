from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()


router.register(r'admins', AdminTgUserViewSet)
router.register(r'helps', HelpTextViewSet)
router.register(r'helpsmedia', HelpTextMediaViewSet)
router.register(r'inlines', InlineMurkupButtonViewSet)
router.register(r'kbuttons', InlineKeyboardMurkupButtonViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
