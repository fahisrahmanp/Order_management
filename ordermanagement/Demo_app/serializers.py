from decimal import Decimal
from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "sku", "price", "stock", "created_at"]

# --- Order / Items ---

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be > 0.")
        return value

class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "subtotal"]

    def get_subtotal(self, obj):
        return (obj.unit_price * obj.quantity)

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "items", "created_at", "updated_at"]
        read_only_fields = ["status", "created_at", "updated_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        bulk_items = []
        for item in items_data:
            product = item["product"]
            qty = item["quantity"]
            bulk_items.append(OrderItem(
                order=order,
                product=product,
                quantity=qty,
                unit_price=product.price,
            ))
        OrderItem.objects.bulk_create(bulk_items)
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = OrderItemReadSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "created_at", "updated_at", "items", "total_amount"]

    def get_total_amount(self, obj):
        return obj.total_amount

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
