from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .models import Customer, Product, Order
from .serializers import (
    CustomerSerializer, ProductSerializer,
    OrderCreateSerializer, OrderDetailSerializer, OrderStatusSerializer
)

class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer").prefetch_related("items__product")
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs.order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        if self.action == "partial_update":
            return OrderStatusSerializer
        return OrderDetailSerializer






# Create your views here.
