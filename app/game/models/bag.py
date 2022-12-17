from django.db.models import Model, DateTimeField
from rest_framework import serializers


class Bag(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    class Meta:
        db_table = '"game"."bag"'
        managed = True

    def __str__(self):
        return self.id



class BagSerializer(serializers.Serializer):
    model = Bag
    fields = '__all__'