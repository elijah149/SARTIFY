from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Vegetable(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
    ]

    day_of_week = models.IntegerField(
        choices=DAYS,
        unique=True
    )

    foods = models.ManyToManyField(
        Food,
        related_name="daily_menus",
        blank=True
    )

    vegetables = models.ManyToManyField(
        Vegetable,
        related_name="daily_menus",
        blank=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week"]

    def __str__(self):
        return self.get_day_of_week_display()
