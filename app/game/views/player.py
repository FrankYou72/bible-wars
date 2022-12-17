from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from ..models.player import Player, PlayerSerializer
from ..models.character import Character
from ..models.match import Match


class BaseViewSet(APIView):
    permission_classes = []


class PlayerViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        character_id = params.get('character_id')
        match_id = params.get('match_id')
        level = params.get('level')
        score = params.get('score')
        lives = params.get('lives')
        is_alive = params.get('is_alive')
        user_id = params.get('user_id')
        order_by = params.get('order_by', '-id')

        players = Player.objects

        if character_id:
            players = players.filter(character_id=character_id)
        if match_id:
            players = players.filter(match_id=match_id)
        if level:
            players = players.filter(level=level)
        if score:
            players = players.filter(score=score)
        if lives:
            players = players.filter(lives=lives)
        if is_alive:
            players = players.filter(is_alive=is_alive)
        if user_id:
            players = players.filter(character_id=user_id)

        players = players.order_by(order_by)

        data = PlayerSerializer(players, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        character_id = data.get('character_id')
        match_id = data.get('match_id')
        level = data.get('level')
        score = data.get('score')
        lives = data.get('lives')
        is_alive = data.get('is_alive')
        user_id = data.get('user_id')

        try:
            character = Character.objects.get(id=character_id)
        except ObjectDoesNotExist:
            response = {"message": f"Character {character_id} does not exist"}
            return Response(response, 400)

        try:
            match = Match.objects.get(id=match_id)
        except ObjectDoesNotExist:
            response = {"message": f"Match {match_id} does not exist"}
            return Response(response, 400)

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            response = {"message": f"User {user_id} does not exist"}
            return Response(response, 400)

        player = Player()
        player.character = character
        player.match = match
        player.level = level
        player.score = score
        player.lives = lives
        player.is_alive = is_alive
        player.save()

        response = PlayerSerializer(player).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        player_id = data.get('player_id')
        character_id = data.get('character_id')
        match_id = data.get('match_id')
        level = data.get('level')
        score = data.get('score')
        lives = data.get('lives')
        is_alive = data.get('is_alive')
        user_id = data.get('user_id')

        try:
            player = Player.objects.get(id=player_id)
        except ObjectDoesNotExist:
            response = {"message": "Player not found"}
            return Response(response, 404)

        if not Character.objects.filter(id=character_id).exists():
            character_id = None
        if not Match.objects.filter(id=match_id).exists():
            match_id = None
        if not User.objects.filter(id=character_id).exists():
            user_id = None

        player.character_id = character_id or player.character_id
        player.match_id = match_id or player.match_id
        player.level = level or player.level
        player.score = score or player.score
        player.lives = lives or player.score
        player.is_alive = is_alive or player.is_alive
        player.save()

        response = PlayerSerializer(player).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        player_id = data.get('player_id')

        try:
            player = Player.objects.get(id=player_id)
        except ObjectDoesNotExist:
            response = {"message": "Player not found"}
            return Response(response, 404)

        try:
            player.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Player {player_id} deleted"}
        return Response(response, 200)
