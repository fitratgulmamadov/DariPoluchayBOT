from django.contrib import admin
from .models import *


admin.site.register([AdminTgUser, HelpText, InlineKeyboardMurkupButton, InlineMurkupButton, HelpTextMedia])