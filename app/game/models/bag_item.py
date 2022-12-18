from django.db.models import Model, ForeignKey, PROTECT
from rest_framework import serializers

from .bag import Bag, BagSerializer
from .item import Item, ItemSerializer


class BagItem(Model):
    bag = ForeignKey(Bag, on_delete=PROTECT, null=True)
    item = ForeignKey(Item, on_delete=PROTECT, null=True)

    class Meta:
        db_table = '"game"."bag_item"'
        managed = True

    def __str__(self):
        return f'{self.bag}: {self.item}'



class BagItemSerializer(serializers.Serializer):
    model = BagItem
    item = ItemSerializer()
    fields = '__all__'