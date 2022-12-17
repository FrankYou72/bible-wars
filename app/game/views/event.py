from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models.event import Event, EventSerializer
from ..models.consequence import Consequence
from ..models.requirement import Requirement


class BaseViewSet(APIView):
    permission_classes = []


class EventViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        name = params.get('name')
        description = params.get('description')
        requirement_id = params.get('requirement_id')
        consequence_id = params.get('consequence_id')
        spiritual_intervention = params.get('spiritual_intervention')
        is_global = params.get('is_global')
        order_by = params.get('order_by', '-id')

        events = Event.objects

        if name:
            events = events.filter(name__icontains=name)
        if description:
            events = events.filter(description__icontains=description)
        if requirement_id:
            events = events.filter(requirement_id=requirement_id)
        if consequence_id:
            events = events.filter(consequence_id=consequence_id)
        if spiritual_intervention:
            events = events.filter(spiritual_intervention=spiritual_intervention)
        if is_global:
            events = events.filter(is_global=is_global)

        events = events.order_by(order_by)

        data = EventSerializer(events, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        description = data.get('description')
        requirement_id = data.get('requirement_id')
        consequence_id = data.get('consequence_id')
        spiritual_intervention = data.get('spiritual_intervention')
        is_global = data.get('is_global')
        order_by = data.get('order_by', '-id')

        try:
            consequence = Consequence.objects.get(id=consequence_id)
        except ObjectDoesNotExist:
            response = {"message": f"Consequence {consequence_id} does not exist"}
            return Response(response, 400)

        try:
            requirement = Requirement.objects.get(id=requirement_id)
        except ObjectDoesNotExist:
            response = {"message": f"Requirement {requirement_id} does not exist"}
            return Response(response, 400)

        event = Event()
        event.name = name
        event.description = description
        event.requirement = requirement
        event.consequence = consequence
        event.spiritual_intervention = spiritual_intervention
        event.is_global = is_global
        event.save()

        response = EventSerializer(event).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        event_id = data.get('event_id')
        name = data.get('name')
        description = data.get('description')
        requirement_id = data.get('requirement_id')
        consequence_id = data.get('consequence_id')
        spiritual_intervention = data.get('spiritual_intervention')
        is_global = data.get('is_global')

        try:
            event = Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            response = {"message": "Event not found"}
            return Response(response, 404)

        if not Consequence.objects.filter(id=consequence_id).exists():
            consequence_id = None
        if not Requirement.objects.filter(id=consequence_id).exists():
            requirement_id = None

        event.name = name or event.name
        event.description = description or event.description
        event.requirement_id = requirement_id or event.requirement_id
        event.consequence_id = consequence_id or event.consequence_id
        event.spiritual_intervention = spiritual_intervention or event.spiritual_intervention
        event.is_global = is_global or event.is_global
        event.save()

        response = EventSerializer(event).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        event_id = data.get('event_id')

        try:
            event = Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            response = {"message": "Event not found"}
            return Response(response, 404)

        try:
            event.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Event {event_id} deleted"}
        return Response(response, 200)
