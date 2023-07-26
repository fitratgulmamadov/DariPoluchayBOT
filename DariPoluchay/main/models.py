from datetime import datetime
from django.db import models


class Board(models.Model):
    name = models.CharField("Board name", max_length=250)
    present_price = models.IntegerField("Present price")
    state = models.IntegerField(unique=True)
    max_present_red = models.IntegerField()
    img = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name





class TgUser(models.Model):
    name = models.CharField('Name', max_length=150)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    ch_id = models.IntegerField("ChatId")
    join_date = models.DateTimeField("Join time", auto_now_add=True)
    link = models.CharField('Link', max_length=150)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    st_CHOICES = [
        ("R", "Red"),
        ("G", "Green"),
        ("W", "White"),
        ("V", "Void")
    ]
    status = models.CharField('Status', choices=st_CHOICES, max_length=1, default="W")

    def __str__(self) -> str:
        return self.name    


class Present(models.Model):
    name = models.CharField(max_length=200, unique=True)
    board = models.ForeignKey(Board, on_delete=models.PROTECT, blank=True, null=True)
    to_user = models.ForeignKey(TgUser, on_delete=models.PROTECT, blank=True, null=True)
    from_user = models.ForeignKey(TgUser, on_delete=models.PROTECT, related_name='from_usr', blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class PassedBoardHistory(models.Model):
    tguser = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    earn = models.IntegerField(blank=True, null=True)



class RefLinks(models.Model):
    tguser = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

    # def save(self, *args, **kwargs):
    #     self.url = f'{self.tguser.ch_id}_{int(datetime.now().timestamp())}' 
    #     super().save(self, *args, **kwargs)
    
