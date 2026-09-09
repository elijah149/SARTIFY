from django.contrib import admin

from .models import Food, Vegetable, DailyMenu


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Food Information",
            {
                "fields": (
                    "name",
                    "description",
                    "is_active",
                )
            }
        ),
    )


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Side Information",
            {
                "fields": (
                    "name",
                    "is_active",
                )
            }
        ),
    )


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):

    list_display = (
        "day_of_week",
        "is_active",
    )

    list_filter = (
        "day_of_week",
        "is_active",
    )

    filter_horizontal = (
        "foods",
        "vegetables",
    )

    fieldsets = (
        (
            "Daily Menu",
            {
                "fields": (
                    "day_of_week",
                    "foods",
                    "vegetables",
                    "is_active",
                )
            }
        ),
    )
