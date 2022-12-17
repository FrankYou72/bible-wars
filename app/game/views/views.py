from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.match import Match, MatchSerializer


class BaseViewSet(APIView):
    permission_classes = []


class MatchViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        nick_name = params.get('nick_name')
        turn_of = params.get('turn_of')
        ended = params.get('ended')
        order_by = params.get('order_by', '-created')

        matches = Match.objects

        if nick_name:
            matches = matches.filter(nick_name=nick_name)
        if turn_of:
            matches = matches.filter(turn_of=turn_of)
        if ended:
            matches = matches.filter(ended=ended)

        matches = matches.order_by(order_by)

        data = MatchSerializer(matches, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        nick_name = data.get('nick_name')

        match = Match()
        match.nick_name = nick_name
        match.save()

        response = MatchSerializer(match).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        match_id = data.get('match_id')
        nick_name = data.get('nick_name')
        turn_of = data.get('turn_of')
        ended = data.get('ended')

        try:
            match = Match.objects.get(id=match_id)
        except ObjectDoesNotExist:
            response = {"message": "Match not found"}
            return Response(response, 404)

        match.nick_name = nick_name or match.nick_name
        match.turn_of = turn_of or match.turn_of
        match.ended = ended or match.ended
        match.save()

        response = MatchSerializer(match).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        match_id = data.get('match_id')

        try:
            match = Match.objects.get(id=match_id)
        except ObjectDoesNotExist:
            response = {"message": "Match not found"}
            return Response(response, 404)

        try:
            match.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Match {match_id} deleted"}
        return Response(response, 200)
