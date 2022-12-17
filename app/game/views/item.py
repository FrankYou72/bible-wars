from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.item import Item, ItemSerializer
from ..models.consequence import Consequence


class BaseViewSet(APIView):
    permission_classes = []


class ItemViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        name = params.get('name')
        description = params.get('description')
        consequence_id = params.get('consequence_id')
        _type = params.get('type')
        _range = params.get('range')
        rarity = params.get('rarity')
        span = params.get('span')
        order_by = params.get('order_by', '-id')

        items = Item.objects

        if name:
            items = items.filter(name__icontains=name)
        if description:
            items = items.filter(description__icontains=description)
        if consequence_id:
            items = items.filter(consequence_id=consequence_id)
        if _type:
            items = items.filter(type=_type)
        if _range:
            items = items.filter(range=_range)
        if rarity:
            items = items.filter(rarity=rarity)
        if span:
            items = items.filter(span=span)

        items = items.order_by(order_by)

        data = ItemSerializer(items, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        description = data.get('description')
        consequence_id = data.get('consequence_id')
        _type = data.get('type')
        _range = data.get('range')
        rarity = data.get('rarity')
        span = data.get('span')
        order_by = data.get('order_by', '-id')

        try:
            consequence = Consequence.objects.get(id=consequence_id)
        except ObjectDoesNotExist:
            response = {"message": f"Consequence {consequence_id} does not exist"}
            return Response(response, 400)

        item = Item()
        item.name = name
        item.description = description
        item.type = _type
        item.range = _range
        item.rarity = rarity
        item.consequence = consequence
        item.span
        item.save()

        response = ItemSerializer(item).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        item_id = data.get('item_id')
        name = data.get('name')
        description = data.get('description')
        consequence_id = data.get('consequence_id')
        _type = data.get('type')
        _range = data.get('range')
        rarity = data.get('rarity')
        span = data.get('span')

        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            response = {"message": "Item not found"}
            return Response(response, 404)

        if not Consequence.objects.filter(id=consequence_id).exists():
            consequence_id = None

        item.name = name or item.name
        item.description = description or item.description
        item.type = _type or item.type
        item.range = _range or item.range
        item.rarity = rarity or item.rarity
        item.consequence_id = consequence_id or item.consequence_id
        item.span = span or item.span
        item.save()

        response = ItemSerializer(item).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        item_id = data.get('item_id')

        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            response = {"message": "Item not found"}
            return Response(response, 404)

        try:
            item.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Item {item_id} deleted"}
        return Response(response, 200)
