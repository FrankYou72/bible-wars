from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.character_class import CharacterClass, CharacterClassSerializer
from ..models.consequence import Consequence


class BaseViewSet(APIView):
    permission_classes = []


class CharacterClassViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        name = params.get('name')
        consequence_id = params.get('consequence_id')
        order_by = params.get('order_by', '-id')

        character_classes = CharacterClass.objects

        if name:
            character_classes = character_classes.filter(name__icontains=name)
        if consequence_id:
            character_classes = character_classes.filter(consequence_id=consequence_id)

        character_classes = character_classes.order_by(order_by)

        data = CharacterClassSerializer(character_classes, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        consequence_id = data.get('consequence_id')

        try:
            consequence = Consequence.objects.get(id=consequence_id)
        except ObjectDoesNotExist:
            response = {"message": f"Consequence {consequence_id} does not exist"}
            return Response(response, 400)

        character_class = CharacterClass()
        character_class.name = name
        character_class.consequence = consequence
        character_class.save()

        response = CharacterClassSerializer(character_class).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        class_id = data.get('class_id')
        name = data.get('name')
        consequence_id = data.get('consequence_id')

        try:
            character_class = CharacterClass.objects.get(id=class_id)
        except ObjectDoesNotExist:
            response = {"message": "CharacterClass not found"}
            return Response(response, 404)

        if not Consequence.objects.filter(id=consequence_id).exists():
            consequence_id = None

        character_class.name = name or character_class.name
        character_class.consequence_id = consequence_id or character_class.consequence_id
        character_class.save()

        response = CharacterClassSerializer(character_class).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        class_id = data.get('class_id')

        try:
            character_class = CharacterClass.objects.get(id=class_id)
        except ObjectDoesNotExist:
            response = {"message": "CharacterClass not found"}
            return Response(response, 404)

        try:
            character_class.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"CharacterClass {class_id} deleted"}
        return Response(response, 200)
