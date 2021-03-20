from django.conf import settings
from deck.models import Action


def get_id_url_list(Character, context):
    id_url_list = []
    # URLとカードID取得
    for i in range(len(context['object_list'])):
        if Character.objects.filter(code = context['object_list'][i].code).exists():
            code = context['object_list'][i].code
            atk = context['object_list'][i].attack
            cost = context['object_list'][i].cost
            rarity = context['object_list'][i].rarity
            group = context['object_list'][i].group
            picture = Character.objects.values_list('picture', flat=True).get(code=code)
        else:
            break
        image_url = f"{settings.MEDIA_URL}{picture}"
        # image_url_list.append(image_url)
        id_url_list.append({"ID": code, "ATK": atk, "COST": cost, "RARITY": rarity, "GROUP": group, "URL": image_url, "num": 0, "show": False})
    context['id_url_list'] = id_url_list
    # context['image_url_list'] = image_url_list

    return context

def get_action_info(context):
    action_info = []
    obj = Action.objects.all()
    for i in range(len(Action.objects.all())):
        code = obj[i].code
        name = obj[i].name
        group = obj[i].group
        rarity = obj[i].rarity
        cost = obj[i].cost
        picture = obj[i].picture
        image_url = f"{settings.MEDIA_URL}{picture}"
        action_info.append({"ID": code, "NAME": name, "GROUP": group, "RARITY": rarity, "COST": cost, "URL": image_url, "num": 0})
    context['action_info'] = action_info

    return context
        