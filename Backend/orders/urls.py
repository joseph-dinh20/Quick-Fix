# orders/urls.py

from django.urls import path
from .views import OrderCreateView, MyOrdersView

urlpatterns = [
    path("", MyOrdersView.as_view(), name="my-orders"),
    path("create/", OrderCreateView.as_view(), name="create-order"),
]