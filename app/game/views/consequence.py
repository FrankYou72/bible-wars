from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.consequence import Consequence, ConsequenceSerializer


class BaseViewSet(APIView):
    permission_classes = []


class ConsequenceViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        description = params.get('description')
        instance = params.get('instance')
        attribute = params.get('attribute')
        operation = params.get('operation')
        factor = params.get('factor')
        order_by = params.get('order_by', '-id')

        consequences = Consequence.objects

        if description:
            consequences = consequences.filter(description__icontains=description)
        if instance:
            consequences = consequences.filter(instance=instance)
        if attribute:
            consequences = consequences.filter(attribute=attribute)
        if operation:
            consequences = consequences.filter(attribute=operation)
        if factor:
            consequences = consequences.filter(attribute=factor)

        consequences = consequences.order_by(order_by)

        data = ConsequenceSerializer(consequences, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        description = data.get('description')
        instance = data.get('instance')
        attribute = data.get('attribute')
        operation = data.get('operation')
        factor = data.get('factor')

        consequence = Consequence()
        consequence.description = description
        consequence.instance = instance
        consequence.attribute = attribute
        consequence.operation = operation
        consequence.factor = factor
        consequence.save()

        response = ConsequenceSerializer(consequence).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        consequence_id = data.get('consequence_id')
        description = data.get('description')
        instance = data.get('instance')
        attribute = data.get('attribute')
        operation = data.get('operation')
        factor = data.get('factor')

        try:
            consequence = Consequence.objects.get(id=consequence_id)
        except ObjectDoesNotExist:
            response = {"message": "Consequence not found"}
            return Response(response, 404)

        consequence.description = description or consequence.description
        consequence.instance = instance or consequence.instance
        consequence.attribute = attribute or consequence.attribute
        consequence.operation = operation or consequence.operation
        consequence.factor = factor or consequence.factor
        consequence.save()

        response = ConsequenceSerializer(consequence).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        consequence_id = data.get('consequence_id')

        try:
            consequence = Consequence.objects.get(id=consequence_id)
        except ObjectDoesNotExist:
            response = {"message": "Consequence not found"}
            return Response(response, 404)

        try:
            consequence.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Consequence {consequence_id} deleted"}
        return Response(response, 200)
