from django.contrib import admin
from .models import *




@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['name', 'present_price', 'state']
    list_display = ['name', 'present_price', 'state']


@admin.register(Present)
class PresentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'board', 'from_user', 'to_user', 'status']
    list_display = ['name', 'board', 'from_user', 'to_user', 'status']


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    search_fields = ['board', 'status']
    list_display = ['name', 'ch_id', 'join_date', 'link', 'board', 'status']

@admin.register(PassedBoardHistory)
class PassedBoardHistory(admin.ModelAdmin):
    search_fields = ['board', 'tguser', 'earn']
    list_display = [ 'tguser', 'board', 'earn']

@admin.register(RefLinks)
class RefLinks(admin.ModelAdmin):
    search_fields = ['tguser', 'url']
    list_display = ['tguser', 'url']
