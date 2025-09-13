from django.urls import path
from .views import CartView, CartItemView, OrderView, PaymentVerifyView

urlpatterns = [
    # --- Cart ---
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("cart/items/", CartItemView.as_view(), name="cartitem-add"),  
    path("cart/items/<int:pk>/", CartItemView.as_view(), name="cartitem-manage"),

    # --- Orders ---
    path("order/create/", OrderView.as_view(), name="order-create"),

    # --- Payment Verification ---
    
]
"""path("order/verify/", PaymentVerifyView.as_view(), name="order-verify"),"""