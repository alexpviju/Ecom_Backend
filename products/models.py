from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)  # ✅ Image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)  # ✅ Image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="variants/", blank=True, null=True)  # ✅ Image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="wishlist_entries")
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,null=True,blank=True,related_name="wishlist_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        #  Must have at least one (product or variant)
        if not self.product and not self.variant:
            raise ValueError("Wishlist item must have either a product or a variant.")

        #  Prevent duplicates (same user + product/variant)
        if self.product and not self.variant:
            if Wishlist.objects.filter(user=self.user, product=self.product, variant__isnull=True).exists():
                raise ValueError("This product is already in the wishlist.")

        if self.variant:
            if Wishlist.objects.filter(user=self.user, variant=self.variant).exists():
                raise ValueError("This variant is already in the wishlist.")

        super().save(*args, **kwargs)

    def __str__(self):
        if self.variant:
            return f"{self.user} - {self.variant}"
        return f"{self.user} - {self.product}"