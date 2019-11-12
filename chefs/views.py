from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404

from .models import Chef, MenuItem


@require_GET
def get_collection(request):
    chefs = Chef.objects.all()

    if request.body:
        req = json.loads(request.body)

        if 'subway' in req:
            chefs = chefs.filter(subway=req['subway'])

    mapped = list(map(map_chef, chefs))

    res = {
        'items': mapped,
        'count': len(mapped)
    }

    return JsonResponse(res)


def map_chef(c):
    return {
        'id': c.user_id,
        'fullname': c.get_full_name(),
        'distance_from_subway': c.ditance_from_subway,
        'median_price': c.get_median_price(),
        'avatar_url': ''  # c.user.avatar.url
    }


@method_decorator(csrf_exempt, name='dispatch')
class Index(View):
    def get(self, request, user_id):
        chef = get_object_or_404(Chef, user_id=user_id)

        return JsonResponse(map_chef(chef))

    def put(self, request, user_id):
        if not request.body:
            return HttpResponseBadRequest()

        req = json.loads(request.body)
        chef = get_object_or_404(Chef, user_id=user_id)

        edit_if_exists(chef, req, 'first_name')
        edit_if_exists(chef, req, 'last_name')
        edit_if_exists(chef, req, 'subway')
        edit_if_exists(chef, req, 'address')
        #  edit_if_exists_d(chef, req, 'avatar_url', 'avatar.url')
        edit_if_exists(chef, req, 'inst_token')

        # edit socials
        if 'social' in req:
            social = req['social']
            edit_if_exists_d(chef, social, 'fb', 'contact_fb')
            edit_if_exists_d(chef, social, 'ok', 'contact_ok')
            edit_if_exists_d(chef, social, 'inst', 'contact_inst')
            edit_if_exists_d(chef, social, 'vk', 'contact_vk')
            edit_if_exists(chef, social, 'phone')
            edit_if_exists(chef, social, 'email')

        # edit menu
        if 'menu' in req:
            menu_items = req['menu']
            for m in menu_items:
                menu_item = chef.menu_items.filter(id=m.id).first()
                if menu_item is None:
                    new_m = MenuItem(name=m.name, price=m.price)
                    chef.menu_items.add(new_m)
                else:
                    menu_item.name = m.name
                    menu_item.price = m.price

        chef.save()
        return HttpResponse()

    @staticmethod
    def map_chef(c: Chef):
        if c is None:
            return ''

        menu_items = map(lambda m: {
            'name': m.name,
            'price': m.price,
        }, c.menu_items)

        return {
            'chef_id': c.id,
            'fullname': c.get_full_name(),
            'subway': c.subway,
            'distance_from_subway': c.ditance_from_subway,
            'address': c.address,
            'avatar_url': '',  # c.avatar.url,
            'social': {
                'fb': c.contact_fb,
                'ok': c.contact_ok,
                'inst': c.contact_inst,
                'vk': c.contact_vk,
                'phone': c.phone,
                'email': c.email,
            },
            'menu': menu_items,
            'inst_token': '',
        }


def edit_if_exists(obj: Chef, req: dict, field_name: str):
    if field_name in req:
        setattr(obj, field_name, req[field_name])


def edit_if_exists_d(obj: Chef, req: dict, req_name: str, ob_name: str):
    if req_name in req:
        setattr(obj, ob_name, req[req_name])
