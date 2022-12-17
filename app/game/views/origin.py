from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.origin import Origin, OriginSerializer
from ..models.consequence import Consequence


class BaseViewSet(APIView):
    permission_classes = []


class OriginViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        name = params.get('name')
        consequence_id = params.get('consequence_id')
        order_by = params.get('order_by', '-id')

        origins = Origin.objects

        if name:
            origins = origins.filter(number__icontains=name)
        if consequence_id:
            origins = origins.filter(consequence_id=consequence_id)

        origins = origins.order_by(order_by)

        data = OriginSerializer(origins, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        consequence_id = data.get('consequence_id')

        if consequence_id:
            try:
                consequence = Consequence.objects.get(id=consequence_id)
            except ObjectDoesNotExist:
                response = {"message": f"Consequence {consequence_id} does not exist"}
                return Response(response, 400)
        else:
            consequence = None

        origin = Origin()
        origin.name = name
        origin.consequence = consequence
        origin.save()

        response = OriginSerializer(origin).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        origin_id = data.get('origin_id')
        name = data.get('name')
        consequence_id = data.get('consequence_id')

        try:
            origin = Origin.objects.get(id=origin_id)
        except ObjectDoesNotExist:
            response = {"message": "Origin not found"}
            return Response(response, 404)

        if not Consequence.objects.filter(id=consequence_id).exists():
            consequence_id = None

        origin.name = name or origin.name
        origin.consequence_id = consequence_id or origin.consequence_id
        origin.save()

        response = OriginSerializer(origin).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        origin_id = data.get('origin_id')

        try:
            origin = Origin.objects.get(id=origin_id)
        except ObjectDoesNotExist:
            response = {"message": "Origin not found"}
            return Response(response, 404)

        try:
            origin.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Origin {origin_id} deleted"}
        return Response(response, 200)
