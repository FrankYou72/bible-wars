from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.body import Body, BodySerializer


class BaseViewSet(APIView):
    permission_classes = []


class BodyViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        head = params.get('head')
        cover = params.get('cover')
        left_arm = params.get('left_arm')
        right_arm = params.get('right_arm')
        feet = params.get('feet')
        order_by = params.get('order_by', '-id')

        bodies = Body.objects

        if head:
            bodies = bodies.filter(head=head)
        if cover:
            bodies = bodies.filter(cover=cover)
        if left_arm:
            bodies = bodies.filter(left_arm=left_arm)
        if right_arm:
            bodies = bodies.filter(right_arm=right_arm)
        if feet:
            bodies = bodies.filter(feet=feet)

        bodies = bodies.order_by(order_by)

        data = BodySerializer(bodies, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data

        body = Body()
        body.save()

        response = BodySerializer(body).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        body_id = data.get('body_id')
        head = data.get('head')
        cover = data.get('cover')
        left_arm = data.get('left_arm')
        right_arm = data.get('right_arm')
        feet = data.get('feet')

        try:
            body = Body.objects.get(id=body_id)
        except ObjectDoesNotExist:
            response = {"message": "Body not found"}
            return Response(response, 404)

        body.head = head or body.head
        body.cover = cover or body.cover
        body.left_arm = left_arm or body.left_arm
        body.right_arm = right_arm or body.right_arm
        body.feet = feet or body.feet
        body.save()

        response = BodySerializer(body).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        body_id = data.get('body_id')

        try:
            body = Body.objects.get(id=body_id)
        except ObjectDoesNotExist:
            response = {"message": "Body not found"}
            return Response(response, 404)

        try:
            body.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Body {body_id} deleted"}
        return Response(response, 200)
