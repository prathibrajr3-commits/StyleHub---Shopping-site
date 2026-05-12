from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, NewsletterSubscriber, ContactMessage, BlogPost
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock', 'is_featured', 'is_new_arrival']
    list_filter = ['category', 'gender', 'is_featured', 'is_new_arrival']
    list_editable = ['price', 'stock', 'is_featured', 'is_new_arrival']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'size', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'total', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    list_editable = ['status']
    search_fields = ['order_number', 'email', 'first_name', 'last_name']
    readonly_fields = ['order_number', 'subtotal', 'shipping', 'total', 'created_at']
    inlines = [OrderItemInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'total_items', 'total_price', 'created_at']
    readonly_fields = ['session_key', 'created_at', 'updated_at']


@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_at', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
