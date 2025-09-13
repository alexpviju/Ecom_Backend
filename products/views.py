from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Category, Product, ProductVariant,Wishlist
from .serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer,WishlistSerializer


# ------------------- CATEGORY -------------------
class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = Category.objects.all().order_by("-created_at")
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategoryUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"message":f"{pk} - Deleted"},status=status.HTTP_204_NO_CONTENT)


# ------------------- PRODUCT -------------------
class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = Product.objects.all().order_by("-created_at")
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message":f"{pk} Deleted"},status=status.HTTP_204_NO_CONTENT)


# ------------------- PRODUCT VARIANT -------------------
class ProductVariantListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = ProductVariant.objects.all().order_by("-created_at")
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(color__icontains=search) | Q(description__icontains=search)
            )
        serializer = ProductVariantSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductVariantCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data)


class ProductVariantUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantSerializer(variant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        variant.delete()
        return Response({"message": f"{pk} Deleted"},status=status.HTTP_204_NO_CONTENT)



#------------------WISHLIST---------------------


class WishlistListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user).order_by("-created_at")
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(Wishlist, pk=pk, user=request.user)
        item.delete()
        return Response({"message": "Item removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)