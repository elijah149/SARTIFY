from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "order_date",
        "food",
        "vegetable",
        "quantity",
        "status",
        "created_at",
    )

    list_filter = (
        "order_date",
        "status",
        "food",
        "vegetable",
    )

    search_fields = (
        "user__username",
        "food__name",
        "vegetable__name",
    )

    date_hierarchy = "order_date"

    list_per_page = 25

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "user",
                    "order_date",
                    "food",
                    "vegetable",
                    "quantity",
                )
            }
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "special_request",
                    "status",
                    "created_at",
                )
            }
        ),
    )
