from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
        
class Character(models.Model):
    rarity_choices = (
        ("1", 'B'), ("2", 'A'), ("3", 'S'), ("4", 'SS')
    )
    group_choices = (
        ('zyuken','287期受験生'),('ryodan','幻影旅団'),('mafian', 'マフィアンコミュニティー'),
        ('gi','G.Iプレイヤー'),('kimera','キメラアント'),('toubatu','蟻と闘う者'),('free','フリー')
    )
    subname = models.CharField(default=None, verbose_name='通り名', max_length=20)
    name = models.CharField(default=None, verbose_name='名前', max_length=20)
    attack = models.IntegerField(default=None, verbose_name='ATK')
    cost = models.IntegerField(default=None, verbose_name='コスト')
    rarity = models.CharField(default=None, verbose_name='レア度', max_length=5, choices=rarity_choices)
    group = models.CharField(default=None, verbose_name='GP', max_length=20, choices=group_choices)
    code = models.IntegerField(default=None, verbose_name='No.', primary_key=True)
    picture = models.ImageField(default=None, upload_to='images/')
    avility = models.TextField(default=None, verbose_name='能力')
    combo = models.TextField(default=None, verbose_name='コンボ')
    num = models.IntegerField(default=0, verbose_name="枚数", blank=True, null=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    rarity_choices = (
        ("1", 'B'), ("2", 'A'), ("3", 'S'), ("4", 'SS')
    )
    group_choices = (
        ('zyuken','287期受験生'),('ryodan','幻影旅団'),('mafian', 'マフィアンコミュニティー'),
        ('gi','G.Iプレイヤー'),('kimera','キメラアント'),('toubatu','蟻と闘う者'),('free','フリー')
    )
    name = models.CharField(default=None, verbose_name='名前', max_length=20)
    cost = models.IntegerField(default=None, verbose_name='コスト')
    rarity = models.CharField(default=None, verbose_name='レア度', max_length=5, choices=rarity_choices)
    group = models.CharField(default=None, verbose_name='GP', max_length=20, choices=group_choices)
    code = models.IntegerField(default=None, verbose_name='No.', primary_key=True)
    picture = models.ImageField(default=None, upload_to='images/')
    avility = models.TextField(default=None, verbose_name='能力')
    num = models.IntegerField(default=0, verbose_name="枚数", blank=True, null=True)

    def __str__(self):
        return self.name

class Deck(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    group = models.CharField(default="", max_length=20, blank=True, null=True)
    title  = models.CharField(default="", max_length=50)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    view_num  = models.IntegerField(default=0, verbose_name="閲覧数", blank=True, null=True)
    like_num = models.IntegerField(default=0, verbose_name="いいね数", blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class DeckOption(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, blank=True, null=True, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.CASCADE)
    character_num = models.IntegerField(default=None, blank=True, null=True)
    action_num = models.IntegerField(default=None, blank=True, null=True)

class Like(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)