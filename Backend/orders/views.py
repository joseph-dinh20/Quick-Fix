# orders/views.py
from rest_framework import generics, permissions
from django.db.models import Q

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer=user) | Q(provider=user)
        ).order_by("-date_completed")