# from django.shortcuts import render, get_object_or_404
# from django.utils import timezone
# from .models import Deck, Card
# from django.conf import settings
# import numpy as np

# def get_decks_card_list(decks):
#     character_card_id_list = [[0 for i in range(24)] for j in range(2)]
#     character_cost_list = [[0 for i in range(24)] for j in range(2)]
#     action_card_id_list = [[0 for i in range(6)] for j in range(2)]
#     action_cost_list = [[0 for i in range(6)] for j in range(2)]

#     j = 0
#     for deck in decks:
#         for i in range(30):
#             if i == 0:
#                 character_card_id_list[j][i] = deck.card1
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card1)
#             elif i == 1:
#                 character_card_id_list[j][i] = deck.card2
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card2)
#             elif i == 2:
#                 character_card_id_list[j][i] = deck.card3
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card3)
#             elif i == 3:
#                 character_card_id_list[j][i] = deck.card4
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card4)
#             elif i == 4:
#                 character_card_id_list[j][i] = deck.card5
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card5)
#             elif i == 5:
#                 character_card_id_list[j][i] = deck.card6
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card6)
#             elif i == 6:
#                 character_card_id_list[j][i] = deck.card7
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card7)
#             elif i == 7:
#                 character_card_id_list[j][i] = deck.card8
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card8)
#             elif i == 8:
#                 character_card_id_list[j][i] = deck.card9
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card9)
#             elif i == 9:
#                 character_card_id_list[j][i] = deck.card10
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card10)
#             elif i == 10:
#                 character_card_id_list[j][i] = deck.card11
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card11)
#             elif i == 11:
#                 character_card_id_list[j][i] = deck.card12
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card12)
#             elif i == 12:
#                 character_card_id_list[j][i] = deck.card13
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card13)
#             elif i == 13:
#                 character_card_id_list[j][i] = deck.card14
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card14)
#             elif i == 14:
#                 character_card_id_list[j][i] = deck.card15
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card15)
#             elif i == 15:
#                 character_card_id_list[j][i] = deck.card16
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card16)
#             elif i == 16:
#                 character_card_id_list[j][i] = deck.card17
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card17)
#             elif i == 17:
#                 character_card_id_list[j][i] = deck.card18
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card18)
#             elif i == 18:
#                 character_card_id_list[j][i] = deck.card19
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card19)
#             elif i == 19:
#                 character_card_id_list[j][i] = deck.card20
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card20)
#             elif i == 20:
#                 character_card_id_list[j][i] = deck.card21
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card21)
#             elif i == 21:
#                 character_card_id_list[j][i] = deck.card22
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card22)
#             elif i == 22:
#                 character_card_id_list[j][i] = deck.card23
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card23)
#             elif i == 23:
#                 character_card_id_list[j][i] = deck.card24
#                 character_cost_list[j][i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card24)

#             elif i == 24:
#                 action_card_id_list[j][0] = deck.action1
#                 action_cost_list[j][0] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action1)
#             elif i == 25:
#                 action_card_id_list[j][1] = deck.action2
#                 action_cost_list[j][1] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action2)
#             elif i == 26:
#                 action_card_id_list[j][2] = deck.action3
#                 action_cost_list[j][2] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action3)
#             elif i == 27:
#                 action_card_id_list[j][3] = deck.action4
#                 action_cost_list[j][3] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action4)
#             elif i == 28:
#                 action_card_id_list[j][4] = deck.action5
#                 action_cost_list[j][4] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action5)
#             elif i == 29:
#                 action_card_id_list[j][5] = deck.action6
#                 action_cost_list[j][5] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action6)
            
#         character_card_id_list[j] = bubble_sort(character_card_id_list[j], character_cost_list[j])
#         print(character_card_id_list)
#         action_card_id_list[j] = bubble_sort(action_card_id_list[j], action_cost_list[j])
#         j += 1

#     return character_card_id_list, action_card_id_list
    

# def get_deck_card_list(deck):
#     character_card_id_list = [0] * 24
#     character_cost_list = [0] * 24
#     action_card_id_list = [0] * 6
#     action_cost_list = [0] * 6

#     for i in range(30):
#         if i == 0:
#             character_card_id_list[i] = deck.card1
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card1)
#         elif i == 1:
#             character_card_id_list[i] = deck.card2
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card2)
#         elif i == 2:
#             character_card_id_list[i] = deck.card3
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card3)
#         elif i == 3:
#             character_card_id_list[i] = deck.card4
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card4)
#         elif i == 4:
#             character_card_id_list[i] = deck.card5
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card5)
#         elif i == 5:
#             character_card_id_list[i] = deck.card6
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card6)
#         elif i == 6:
#             character_card_id_list[i] = deck.card7
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card7)
#         elif i == 7:
#             character_card_id_list[i] = deck.card8
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card8)
#         elif i == 8:
#             character_card_id_list[i] = deck.card9
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card9)
#         elif i == 9:
#             character_card_id_list[i] = deck.card10
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card10)
#         elif i == 10:
#             character_card_id_list[i] = deck.card11
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card11)
#         elif i == 11:
#             character_card_id_list[i] = deck.card12
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card12)
#         elif i == 12:
#             character_card_id_list[i] = deck.card13
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card13)
#         elif i == 13:
#             character_card_id_list[i] = deck.card14
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card14)
#         elif i == 14:
#             character_card_id_list[i] = deck.card15
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card15)
#         elif i == 15:
#             character_card_id_list[i] = deck.card16
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card16)
#         elif i == 16:
#             character_card_id_list[i] = deck.card17
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card17)
#         elif i == 17:
#             character_card_id_list[i] = deck.card18
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card18)
#         elif i == 18:
#             character_card_id_list[i] = deck.card19
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card19)
#         elif i == 19:
#             character_card_id_list[i] = deck.card20
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card20)
#         elif i == 20:
#             character_card_id_list[i] = deck.card21
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card21)
#         elif i == 21:
#             character_card_id_list[i] = deck.card22
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card22)
#         elif i == 22:
#             character_card_id_list[i] = deck.card23
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card23)
#         elif i == 23:
#             character_card_id_list[i] = deck.card24
#             character_cost_list[i] = Card.objects.values_list('cost', flat=True).get(card_id=deck.card24)

#         elif i == 24:
#             action_card_id_list[0] = deck.action1
#             action_cost_list[0] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action1)
#         elif i == 25:
#             action_card_id_list[1] = deck.action2
#             action_cost_list[1] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action2)
#         elif i == 26:
#             action_card_id_list[2] = deck.action3
#             action_cost_list[2] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action3)
#         elif i == 27:
#             action_card_id_list[3] = deck.action4
#             action_cost_list[3] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action4)
#         elif i == 28:
#             action_card_id_list[4] = deck.action5
#             action_cost_list[4] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action5)
#         elif i == 29:
#             action_card_id_list[5] = deck.action6
#             action_cost_list[5] = Card.objects.values_list('cost', flat=True).get(card_id=deck.action6)
            
#     character_card_id_list = bubble_sort(character_card_id_list, character_cost_list)
#     print(character_card_id_list)
#     action_card_id_list = bubble_sort(action_card_id_list, action_cost_list)

#     return character_card_id_list, action_card_id_list

# def bubble_sort(card_id, cost):
#     change = True
#     while change:
#         change = False
#         for i in range(len(cost) - 1):
#             if cost[i] < cost[i + 1]:
#                 cost[i], cost[i + 1] = cost[i + 1], cost[i]
#                 card_id[i], card_id[i + 1] = card_id[i + 1], card_id[i]
#                 change = True
#     return card_id

# def gets_card_image_url_list(decks, character_card_id_list):
#     #card_idからpictureのURLを取得する。  
#     image_url_list = [[0 for i in range(24)] for j in range(2)]
#     for j in range(len(decks)):
#         for i in range(24):
#             picture = Card.objects.values_list('picture', flat=True).get(card_id=character_card_id_list[j][i])
#             image_url = f"{settings.MEDIA_URL}{picture}"
#             image_url_list[j][i] = image_url
    
#     return image_url_list

# def get_card_image_url_list(character_card_id_list):
#     #card_idからpictureのURLを取得する。  
#     image_url_list = [0]*24
#     for i in range(24):
#         picture = Card.objects.values_list('picture', flat=True).get(card_id=character_card_id_list[i])
#         image_url = f"{settings.MEDIA_URL}{picture}"
#         image_url_list[i] = image_url
    
#     return image_url_list