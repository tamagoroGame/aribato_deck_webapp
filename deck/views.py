from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.utils import timezone
from .models import Deck, Character, Tag, DeckOption, Action, Like
from django.conf import settings
# from .myfunc import get_deck_card_list, get_decks_card_list, get_card_image_url_list, gets_card_image_url_list
import numpy as np
from django.views import generic

from .get_id_url_list import get_id_url_list, get_action_info

import json
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.decorators import login_required


import re


# カード詳細ページ
class CardDetailView(generic.DetailView):
    model = Character

# 全カード一覧ページ
class CardListView(generic.ListView):
    model = Character
    template_name = 'deck/card_list.html' 
    paginate_by = 30

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('serch'):
            form_value = {
                'rarity': self.request.POST.getlist('rarity', None),
                'group': self.request.POST.getlist('group', None),
            }
            request.session['form_value'] = form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        # self.request.GET = self.request.GET.copy()
        # self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = get_id_url_list(Character, context)
        context = get_action_info(context)

        characters = Character.objects.all().order_by('-cost', '-group', '-rarity', '-attack', '-code')
        characters_info = []
        for character in characters:
            characters_info.append({
                "ID": character.code,
                "URL": "/media/" + str(character.picture),
                "num": 0,
                "detail": "/card/" + str(character.code),
                "show": False
            })

        actions = Action.objects.all().order_by('-cost', '-group', '-rarity', '-code')
        actions_info = []
        for action in actions:
            actions_info.append({
                "ID": action.code,
                "URL": "/media/" + str(action.picture),
                "num": 0,
                "detail": "/card/" + str(action.code),
                "show": False
            })

        context['characters'] = characters_info
        context['actions'] = actions_info
        
        return context

    def get_queryset(self):
        card_list = Character.objects.all().order_by('code')
        if ('form_value' in self.request.session) and self.request.POST.get('serch'):
            form_value = self.request.session['form_value']
            rarity = form_value['rarity']
            group = form_value['group']
            if len(rarity) != 0:
                card_list = card_list.filter(rarity__in = rarity)
            if len(group) != 0:
                card_list = card_list.filter(group__in = group)
            return card_list
        return card_list

# 全デッキ一覧を表示
class DeckListView(generic.ListView):
    model = Deck
    template_name = "deck/deck_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        decks_order_by_like_num = Deck.objects.filter(published_date__lte=timezone.now()).order_by('-like_num')
        decks_order_by_created_date = Deck.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')

        order_by_created_date = []
        for deck in decks_order_by_created_date:
            order_by_created_date.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        order_by_like_num = []
        for deck in decks_order_by_like_num:
            order_by_like_num.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        context['order_by'] = {
            'created_date': order_by_created_date,
            'like_num': order_by_like_num
        }  

        return context

    # def get_queryset(self):
    #     decks = Deck.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
    #     return decks

# デッキ詳細
class DeckDetailView(generic.DetailView):
    model = Deck
    template_name = "deck/deck_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        o = DeckOption.objects.filter(deck=self.kwargs.get('pk', ''))
        context['card_list'] = o.filter(action=None)
        context['action_list'] = o.filter(character=None)
        context['option_list'] = o

        if self.request.user.is_authenticated:
            like = Like.objects.filter(deck__id=self.kwargs.get('pk',''), user=self.request.user)
            like_flag = len(like)
        else:
            like_flag = 0

        like_num = len(Like.objects.filter(deck__id=self.kwargs.get('pk','')))

        context['like_flag'] = like_flag
        context['like_num'] = like_num

        return context


# デッキ作成
class DeckNewView(generic.ListView):
    model = Character
    template_name = 'deck/deck_new.html' 
    # paginate_by = 30

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')

        return super().get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account_login')

        if self.request.POST.get('serch'):
            form_value = {
                'rarity': self.request.POST.getlist('rarity', None),
                'group': self.request.POST.getlist('group', None),
            }
            request.session['form_value'] = form_value

        # デッキ作成の時
        if len(self.request.POST.get('card_id_list')) != 0:
            id_list = request.POST.get('card_id_list',None).split(',')
            num_list = request.POST.get('card_num_list',None).split(',')
            action_id_list = request.POST.get('action_id_list',None).split(',')
            action_num_list = request.POST.get('action_num_list',None).split(',')

            characters = Character.objects.filter(code__in=id_list)
            group_list = {
                "ryodan": 0,
                "zyuken": 0,
                "mafian": 0,
                "gi": 0,
                "kimera": 0,
                "toubatu": 0,
                "free": 0,
            }
            i = 0
            for character in characters:
                group_list[character.group]+=int(num_list[i])
                i+=1

            max_k_list = [kv[0] for kv in group_list.items() if kv[1] == max(group_list.values())]

            print(max_k_list)

            user = request.user
            deck = Deck(author=user, title=request.POST.get('title'))
            deck.published_date = timezone.now()
            if len(max_k_list) > 1:
                print("free")
                deck.group = "free"
            else:
                print(max_k_list[0])
                deck.group = max_k_list[0]
            deck.save()

            for i in range(len(id_list)):
                o = DeckOption()
                o.deck = deck
                o.character = Character.objects.get(code=id_list[i])
                o.character_num = int(num_list[i])
                o.save()
                
            for i in range(len(action_id_list)):
                o = DeckOption()
                o.deck = deck
                o.action = Action.objects.get(code=action_id_list[i])
                o.action_num = int(action_num_list[i])
                o.save()
                
            # return redirect('deck_detail', pk=deck.pk)
            return redirect('deck_list')

        # 検索時にページネーションに関連したエラーを防ぐ
        # self.request.GET = self.request.GET.copy()
        # self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context = get_id_url_list(Character, context)

        context['tags'] = Tag.objects.all()
        context = get_action_info(context)

        characters = Character.objects.all().order_by('-cost', '-group', '-rarity', '-attack', '-code')
        characters_info = []
        for character in characters:
            characters_info.append({
                "ID": character.code,
                "URL": "/media/" + str(character.picture),
                "num": 0,
                "detail": "/card/" + str(character.code),
                "show": False
            })

        actions = Action.objects.all().order_by('-cost', '-group', '-rarity', '-code')
        actions_info = []
        for action in actions:
            actions_info.append({
                "ID": action.code,
                "URL": "/media/" + str(action.picture),
                "num": 0,
                "detail": "/card/" + str(action.code),
                "show": False
            })

        context['characters'] = characters_info
        context['actions'] = actions_info
        
        return context

    def get_queryset(self):
        card_list = Character.objects.all().order_by('code')
        if ('form_value' in self.request.session) and self.request.POST.get('serch'):
            form_value = self.request.session['form_value']
            rarity = form_value['rarity']
            group = form_value['group']
            if len(rarity) != 0:
                card_list = card_list.filter(rarity__in = rarity)
            if len(group) != 0:
                card_list = card_list.filter(group__in = group)
            return card_list
        return card_list

# マイページ
class MypageView(generic.ListView):
    model=Deck
    template_name="deck/mypage.html"

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            print("ログインしていません。")
            return redirect('account_login')

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        user = self.request.user

        decks_order_by_like_num = Deck.objects.filter(published_date__lte=timezone.now(), author=user.id).order_by('-like_num')
        decks_order_by_created_date = Deck.objects.filter(published_date__lte=timezone.now(), author=user.id).order_by('-created_date')

        order_by_created_date = []
        for deck in decks_order_by_created_date:
            order_by_created_date.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "tag": deck.group,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "/deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        order_by_like_num = []
        for deck in decks_order_by_like_num:
            order_by_like_num.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "tag": deck.group,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "/deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        context['order_by'] = {
            'created_date': order_by_created_date,
            'like_num': order_by_like_num,
        }
        context['user_id'] = user.id

        return context
def LikeView(request):
    if request.method =="POST":
        if request.user.is_authenticated:
            deck = get_object_or_404(Deck, pk=request.POST.get('deck_id'))
            user = request.user
            liked = False
            like = Like.objects.filter(deck=deck, user=user)
            if like.exists():
                like.delete()
                deck.like_num -= 1
                deck.save()
            else:
                like.create(deck=deck, user=user)
                liked = True
                deck.like_num += 1
                deck.save()

            context={
                'deck_id': deck.id,
                'liked': liked,
                'count': deck.like_set.count(),
                'is_authenticated': True
            }

            if request.is_ajax():
                return JsonResponse(context)
        else:
            context={
                'is_authenticated': False
            }
            if request.is_ajax():
                return JsonResponse(context)


def DeckOrderByView(request):
    if request.method == "POST":
        if request.POST.get('order_by') == "like_num":
            if request.POST.get('mypage') == True:
                decks = Deck.objects.filter(author=request.POST.get('user_id')).order_by('-like_num')
                deck_info = []
                for deck in decks:
                    deck_info.append({
                        "id": deck.id, 
                        "title": deck.title,
                        "author": deck.author.username,
                        "created_date": deck.created_date,
                        "group": "/media/images/" + deck.group + ".webp",
                        "detail_url": "deck/" + str(deck.id),
                        "like_num": deck.like_num,
                        "user_id": request.POST.get('user_id')
                        })
                context = {
                    'decks': deck_info
                }  
            else:        
                decks = Deck.objects.all().order_by('-like_num')
                deck_info = []
                for deck in decks:
                    deck_info.append({
                        "id": deck.id, 
                        "title": deck.title,
                        "author": deck.author.username,
                        "created_date": deck.created_date,
                        "group": "/media/images/" + deck.group + ".webp",
                        "detail_url": "deck/" + str(deck.id),
                        "like_num": deck.like_num,
                        })
                context = {
                    'decks': deck_info
                }
            return JsonResponse(context)
    context={}
    return JsonResponse(context)

def NumChangeView(request):
    if request.method == "POST":
        if request.POST.get('card') == 'character':
            character = get_object_or_404(Character, code=request.POST.get('ID'))
            character.num += 1
            show = True
            if character.num == 3:
                character.num = 0
                show = False
            character.save()
            context = {
                'num': character.num,
                'show': show,
            }
            return JsonResponse(context)

        elif request.POST.get('card') == 'action':
            action = get_object_or_404(Action, code=request.POST.get('ID'))
            action.num += 1
            show = True
            if action.num == 3:
                action.num = 0
                show = False
            action.save()
            context = {
                'num': action.num,
                'show': show,
            }
            return JsonResponse(context)

def NumReset(request):
    if request.method == "POST":
        characters = Character.objects.filter(num__gte = 1)
        for character in characters:
            character.num = 0
            character.save()

        actions = Action.objects.filter(num__gte = 1)
        for action in actions:
            action.num = 0
            action.save()
        
        return JsonResponse({'success': True})

def deck_narrowing(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id', None)
        print("ssssss",user_id)
        #デッキを取得
        decks_like_num_list = json.loads(request.POST.get('like_num', None))
        decks_created_date_list = json.loads(request.POST.get('created_date', None))

        # グループリストを取得
        group_list = request.POST.getlist('group', None)
        group_list = re.sub('["]', "", "".join(group_list[0]))
        group_list = group_list.replace("[", "")
        group_list = group_list.replace("]", "")
        group_list = group_list.split(",")
        if group_list == ['']:
            group_list = Character.objects.all().values_list('group', flat=True).distinct()

        decks_like_num = Deck.objects.filter(group__in=group_list, author=user_id).order_by('-like_num')
        decks_created_date = Deck.objects.filter(group__in=group_list, author=user_id).order_by('-created_date')

        print(decks_like_num)

        order_by_created_date = []
        for deck in decks_created_date:
            order_by_created_date.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "tag": deck.group,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        order_by_like_num = []
        for deck in decks_like_num:
            order_by_like_num.append({
                "id": deck.id, 
                "title": deck.title,
                "author": deck.author.username,
                "created_date": deck.created_date,
                "tag": deck.group,
                "group": "/media/images/" + deck.group + ".webp",
                "detail_url": "deck/" + str(deck.id),
                "like_num": deck.like_num,
                })

        context = {}
        context['order_by'] = {
            'created_date': order_by_created_date,
            'like_num': order_by_like_num
        }

        return JsonResponse(context)

def Narrowing(request):
    if request.method == "POST":
        # カードを取得
        selected_characters = json.loads(request.POST.getlist('selected_characters', None)[0])
        selected_actions = json.loads(request.POST.getlist('selected_actions', None)[0])

        # レアリティリストを取得
        rarity_list = request.POST.getlist('rarity', None)
        rarity_list = re.sub('["]', "", "".join(rarity_list[0]))
        rarity_list = rarity_list.replace("[", "")
        rarity_list = rarity_list.replace("]", "")
        rarity_list = rarity_list.split(",")
        if rarity_list == ['']:
            rarity_list = Character.objects.all().values_list('rarity', flat=True).distinct()

        # グループリストを取得
        group_list = request.POST.getlist('group', None)
        group_list = re.sub('["]', "", "".join(group_list[0]))
        group_list = group_list.replace("[", "")
        group_list = group_list.replace("]", "")
        group_list = group_list.split(",")
        if group_list == ['']:
            group_list = Character.objects.all().values_list('group', flat=True).distinct()

        # 並び替え・昇順降順を取得
        order_by = request.POST.get('order_by', None)
        order_key = request.POST.get('order_key', None)
        if order_key == "DESCEND":
            if order_by == "cost":
                characters = Character.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('-cost', '-group', '-rarity', '-attack', '-code')
                characters_select = Character.objects.all().order_by('-cost', '-group', '-rarity', '-attack', '-code')
                actions = Action.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('-cost', '-group', '-rarity', '-code')
                actions_select = Action.objects.all().order_by('-cost', '-group', '-rarity', '-code')
            if order_by == "rarity":
                characters = Character.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('-rarity', '-group', '-cost', '-attack', '-code')
                characters_select = Character.objects.all().order_by('-rarity', '-group', '-cost', '-attack', '-code')
                actions = Action.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('-rarity', '-group', '-cost', '-code')
                actions_select = Action.objects.all().order_by('-rarity', '-group', '-cost', '-code')

        else:
            if order_by == "cost":
                characters = Character.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('cost', 'group', 'rarity', 'attack', 'code')
                characters_select = Character.objects.all().order_by('cost', 'group', 'rarity', 'attack', 'code')
                actions = Action.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('cost', 'group', 'rarity', 'code')
                actions_select = Action.objects.all().order_by('cost', 'group', 'rarity', 'code')
            if order_by == "rarity":
                characters = Character.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('rarity', 'group', 'cost', 'attack', 'code')
                characters_select = Character.objects.all().order_by('rarity', 'group', 'cost', 'attack', 'code')
                actions = Action.objects.filter(group__in=group_list, rarity__in=rarity_list).order_by('rarity', 'group', 'cost', 'code')
                actions_select = Action.objects.all().order_by('rarity', 'group', 'cost', 'code')

        characters_info = []
        for character in characters:
            characters_info.append({
                "ID": character.code,
                "URL": "/media/" + str(character.picture),
                "num": character.num,
                "detail": "/card/" + str(character.code),
                "show": False
            })

        selected_characters_info = []
        for character in characters_select:
            selected_characters_info.append({
                "ID": character.code,
            })

        actions_info = []
        for action in actions:
            actions_info.append({
                "ID": action.code,
                "URL": "/media/" + str(action.picture),
                "num": action.num,
                "detail": "/card/" + str(action.code),
                "show": False
            })

        selected_actions_info = []
        for action in actions_select:
            selected_actions_info.append({
                "ID": action.code,
            })

        print(characters)

        context = {}
        context['characters'] = characters_info
        context['selected_characters'] = selected_characters_info
        context['actions'] = actions_info
        context['selected_actions'] = selected_actions_info

        return JsonResponse(context)




