from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.level import Level, LevelSerializer
from ..models.character import Character


class BaseViewSet(APIView):
    permission_classes = []


class LevelViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        number = params.get('number')
        slate = params.get('slate')
        character_id = params.get('character_id')
        order_by = params.get('order_by', '-id')

        levels = Level.objects

        if number:
            levels = levels.filter(number=number)
        if slate:
            levels = levels.filter(slate__icontains=slate)
        if character_id:
            levels = levels.filter(character_id=character_id)

        levels = levels.order_by(order_by)

        data = LevelSerializer(levels, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        number = data.get('number')
        slate = data.get('slate')
        character_id = data.get('character_id')

        try:
            character = Character.objects.get(id=character_id)
        except ObjectDoesNotExist:
            response = {"message": f"Character {character_id} does not exist"}
            return Response(response, 400)

        level = Level()
        level.number = number
        level.slate = slate
        level.character = character
        level.save()

        response = LevelSerializer(level).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        level_id = data.get('level_id')
        number = data.get('number')
        slate = data.get('slate')
        character_id = data.get('character_id')

        try:
            level = Level.objects.get(id=level_id)
        except ObjectDoesNotExist:
            response = {"message": "Level not found"}
            return Response(response, 404)

        if not Character.objects.filter(id=character_id).exists():
            character_id = None

        level.number = number or level.number
        level.slate = slate or level.slate
        level.character_id = character_id or level.character_id
        level.save()

        response = LevelSerializer(level).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        level_id = data.get('level_id')

        try:
            level = Level.objects.get(id=level_id)
        except ObjectDoesNotExist:
            response = {"message": "Level not found"}
            return Response(response, 404)

        try:
            level.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Level {level_id} deleted"}
        return Response(response, 200)
