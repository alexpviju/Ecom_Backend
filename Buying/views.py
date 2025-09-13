from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from products.models import Product, ProductVariant


# --- CART ---
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# --- CART ITEM ---
class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Add product or variant to cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        variant_id = request.data.get("variant")
        quantity = int(request.data.get("quantity", 1))

        if not product_id and not variant_id:
            return Response({"error": "Provide either product or variant"}, status=status.HTTP_400_BAD_REQUEST)

        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
        else:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """Update quantity"""
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        quantity = int(request.data.get("quantity", 1))
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    def delete(self, request, pk):
        """Remove item from cart"""
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)


# --- ORDER ---
import razorpay
from django.conf import settings

class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Create an order with Razorpay"""
        cart = get_object_or_404(Cart, user=request.user)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total
        total_amount = sum([
            (item.variant.price if item.variant else item.product.base_price) * item.quantity
            for item in cart.items.all()
        ])
        amount_in_paise = int(total_amount * 100)  # Razorpay needs paise

        # Create Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create order in Razorpay
        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        # Save order in DB
        order = Order.objects.create(
            user=request.user, 
            cart=cart,
            amount=total_amount,
            razorpay_order_id=razorpay_order["id"]
        )

        data = {
            "order_id": order.id,
            "total_amount": total_amount,
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "currency": "INR"
        }

        return Response(data, status=status.HTTP_201_CREATED)

#verification

import hmac
import hashlib

class PaymentVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.is_paid = True
            order.save()
            return Response({"message": "Payment verified successfully"})
        else:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)
