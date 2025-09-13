from rest_framework import serializers
from .models import Cart, CartItem, Order
from products.models import Product, ProductVariant


# --- PRODUCT SERIALIZERS FOR CART DISPLAY ---
class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "base_price"]


class ProductVariantMiniSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "color", "price", "product"]


# --- CART ITEM ---
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)
    variant = ProductVariantMiniSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "variant", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        price = obj.variant.price if obj.variant else obj.product.base_price
        return price * obj.quantity


# --- CART ---
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_amount"]

    def get_total_amount(self, obj):
        return sum([
            (item.variant.price if item.variant else item.product.base_price) * item.quantity
            for item in obj.items.all()
        ])


# --- ORDER ---
class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "cart", "total_amount", "razorpay_order_id",
            "status", "created_at"
        ]
