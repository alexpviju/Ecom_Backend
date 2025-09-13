from rest_framework import serializers
from .models import Category, Product, ProductVariant,Wishlist


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)  

    class Meta:
        model = Product
        fields = "__all__"

from rest_framework import serializers
from .models import Wishlist, Product, ProductVariant
from .serializers import ProductSerializer, ProductVariantSerializer


class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    variant = ProductVariantSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True, required=False
    )
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(), source="variant", write_only=True, required=False
    )

    price = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "product",
            "variant",
            "product_id",
            "variant_id",
            "price",
            "created_at",
        ]

    def get_price(self, obj):
        """Return correct price"""
        if obj.variant:
            return obj.variant.price
        if obj.product:
            return obj.product.base_price  # or obj.product.price if that's your field
        return None

    def get_product(self, obj):
        """Show only id + name when variant exists, else full product"""
        if obj.variant:
            return {
                "id": obj.variant.product.id,
                "name": obj.variant.product.name,
            }
        if obj.product:
            return ProductSerializer(obj.product).data
        return None
