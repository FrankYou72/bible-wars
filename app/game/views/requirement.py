from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from ..models.requirement import Requirement, RequirementSerializer
from ..models.character_class import CharacterClass


class BaseViewSet(APIView):
    permission_classes = []


class RequirementViewSet(BaseViewSet):
    def get(self, request):
        params = request.query_params
        class_id = params.get('class_id')
        alliance = params.get('alliance')
        attribute = params.get('attribute')
        required = params.get('required')
        order_by = params.get('order_by', '-id')

        requirements = Requirement.objects

        if class_id:
            requirements = requirements.filter(character_class_id=class_id)
        if alliance:
            requirements = requirements.filter(alliance=alliance)
        if attribute:
            requirements = requirements.filter(attribute=attribute)
        if required:
            requirements = requirements.filter(required=required)

        requirements = requirements.order_by(order_by)

        data = RequirementSerializer(requirements, many=True).data

        return Response(data)

    def post(self, request):
        data = request.data
        character_class_id = data.get('class_id')
        alliance = data.get('alliance')
        attribute = data.get('attribute')
        required = data.get('required')

        character_class = character_class_id

        if character_class_id:
            try:
                character_class = CharacterClass.objects.get(id=character_class_id)
            except ObjectDoesNotExist:
                response = {"message": f"CharacterClass {character_class_id} does not exist"}
                return Response(response, 400)

        requirement = Requirement()
        requirement.character_class = character_class
        requirement.alliance = alliance
        requirement.attribute = attribute
        requirement.required = required
        requirement.save()

        response = RequirementSerializer(requirement).data
        return Response(response, 201)

    def put(self, request):
        data = request.data
        requirement_id = data.get('requirement_id')
        character_class_id = data.get('class_id')
        alliance = data.get('alliance')
        attribute = data.get('attribute')
        required = data.get('required')

        try:
            requirement = Requirement.objects.get(id=requirement_id)
        except ObjectDoesNotExist:
            response = {"message": "Requirement not found"}
            return Response(response, 404)

        if not CharacterClass.objects.filter(id=character_class_id).exists():
            character_class_id = None

        requirement.character_class_id = character_class_id or requirement.character_class_id
        requirement.alliance = alliance or requirement.alliance
        requirement.attribute = attribute or requirement.attribute
        requirement.required = required or requirement.required
        requirement.save()

        response = RequirementSerializer(requirement).data
        return Response(response, 200)


    def delete(self, request):
        data = request.data
        requirement_id = data.get('requirement_id')

        try:
            requirement = Requirement.objects.get(id=requirement_id)
        except ObjectDoesNotExist:
            response = {"message": "Requirement not found"}
            return Response(response, 404)

        try:
            requirement.delete()
        except Exception as error:
            response = {"message": f'Error: {error}'}
            return Response(response, 500)

        response = {"message": f"Requirement {requirement_id} deleted"}
        return Response(response, 200)
