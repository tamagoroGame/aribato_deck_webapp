from django.contrib import admin
from .models import Character, Deck, Tag, DeckOption, Action, Like

admin.site.register(Character)
admin.site.register(Deck)
admin.site.register(Tag)
admin.site.register(DeckOption)
admin.site.register(Action)
admin.site.register(Like)
# Register your models here.
