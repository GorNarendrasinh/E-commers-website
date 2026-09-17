from django.contrib import admin
from .models import User, PurchaseOrder


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "mobile", "created_at")
    search_fields = ("username", "email", "mobile")
    list_filter = ("created_at",)


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "mobile",
        "email",
        "city",
        "payment_method",
        "total",
        "status",
        "created_at",
    )

    search_fields = (
        "full_name",
        "mobile",
        "email",
        "city",
        "pincode",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    readonly_fields = (
        "user",
        "full_name",
        "mobile",
        "email",
        "address",
        "city",
        "state",
        "pincode",
        "payment_method",
        "products",
        "subtotal",
        "shipping",
        "total",
        "created_at",
    )

    ordering = ("-created_at",)