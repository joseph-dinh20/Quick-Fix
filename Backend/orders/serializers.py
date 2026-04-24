# orders/serializers.py
from rest_framework import serializers
from .models import Order
from accounts.serializers import ProfileSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer(read_only=True)
    provider = ProfileSerializer(read_only=True)
    display_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_display_amount(self, obj):
      user = self.context["request"].user
      if obj.provider == user:
          return -obj.amount
      return obj.amount


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "provider",
            "job",
            "date_completed",
            "amount",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        return Order.objects.create(
            customer=request.user,
            **validated_data
        )