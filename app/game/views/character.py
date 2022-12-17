from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.character import Character, CharacterSerializer


class BaseViewSet(APIView):
    permission_classes = []


class CharacterViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        name = params.get('name')
        info = params.get('info')
        hp = params.get('hp')
        power = params.get('power')
        wisdom = params.get('wisdom')
        faith = params.get('faith')
        attack = params.get('attack')
        defense = params.get('defense')
        speed = params.get('speed')
        alliance = params.get('alliance')
        is_minion = params.get('is_minion')

        order_by = params.get('order_by', '-id')

        characters = Character.objects

        if name:
            characters = characters.filter(name__icontains=name)
        if info:
            characters = characters.filter(info__icontains=info)
        if hp:
            characters = characters.filter(hp=hp)
        if power:
            characters = characters.filter(power=power)
        if wisdom:
            characters = characters.filter(wisdom=wisdom)
        if faith:
            characters = characters.filter(faith=faith)
        if attack:
            characters = characters.filter(attack=attack)
        if defense:
            characters = characters.filter(defense=defense)
        if speed:
            characters = characters.filter(speed=speed)
        if alliance:
            characters = characters.filter(alliance=alliance)
        if is_minion:
            characters = characters.filter(is_minion=is_minion)

        characters = characters.order_by(order_by)

        data = CharacterSerializer(characters, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        info = data.get('info')
        hp = data.get('hp')
        power = data.get('power')
        wisdom = data.get('wisdom')
        faith = data.get('faith')
        attack = data.get('attack')
        defense = data.get('defense')
        speed = data.get('speed')
        alliance = data.get('alliance')
        is_minion = data.get('is_minion')

        character = Character()
        character.name = name
        character.info = info
        character.hp = hp
        character.power = power
        character.wisdom = wisdom
        character.faith = faith
        character.attack = attack
        character.defense = defense
        character.speed = speed
        character.alliance = alliance
        character.is_minion = is_minion
        character.save()

        response = CharacterSerializer(character).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        character_id = data.get('character_id')
        name = data.get('name')
        info = data.get('info')
        hp = data.get('hp')
        power = data.get('power')
        wisdom = data.get('wisdom')
        faith = data.get('faith')
        attack = data.get('attack')
        defense = data.get('defense')
        speed = data.get('speed')
        alliance = data.get('alliance')
        is_minion = data.get('is_minion')

        try:
            character = Character.objects.get(id=character_id)
        except ObjectDoesNotExist:
            response = {"message": "Character not found"}
            return Response(response, 404)

        character.name = name or character.name
        character.info = info or character.info
        character.hp = hp or character.hp
        character.power = power or character.power
        character.wisdom = wisdom or character.wisdom
        character.faith = faith or character.faith
        character.attack = attack or character.attack
        character.defense = defense or character.defense
        character.speed = speed or character.speed
        character.alliance = alliance or character.alliance
        character.is_minion = is_minion or character.is_minion
        character.save()

        response = CharacterSerializer(character).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        character_id = data.get('character_id')

        try:
            character = Character.objects.get(id=character_id)
        except ObjectDoesNotExist:
            response = {"message": "Character not found"}
            return Response(response, 404)

        try:
            character.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Character {character_id} deleted"}
        return Response(response, 200)
