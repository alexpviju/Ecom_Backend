from django.urls import path
from . import views
from .views import WishlistListCreateView, WishlistDetailView

urlpatterns = [
    # ------------------- CATEGORY -------------------
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),

    # ------------------- PRODUCT -------------------
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),

    # ------------------- PRODUCT VARIANT -------------------
    path("variants/", views.ProductVariantListView.as_view(), name="variant-list"),
    path("variants/create/", views.ProductVariantCreateView.as_view(), name="variant-create"),
    path("variants/<int:pk>/", views.ProductVariantDetailView.as_view(), name="variant-detail"),
    path("variants/<int:pk>/update/", views.ProductVariantUpdateView.as_view(), name="variant-update"),
    path("variants/<int:pk>/delete/", views.ProductVariantDeleteView.as_view(), name="variant-delete"),

    # ------------------- WISHLIST -------------------
    path("wishlist/", WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path("wishlist/<int:pk>/", WishlistDetailView.as_view(), name="wishlist-detail"),

]
