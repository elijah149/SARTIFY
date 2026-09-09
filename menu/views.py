from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Food, Vegetable, DailyMenu


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.is_staff:
            messages.error(
                request,
                "You do not have permission to access this page."
            )
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


@staff_required
def daily_menu(request):
    menus = DailyMenu.objects.all().prefetch_related(
        "foods",
        "vegetables"
    )

    menu_by_day = {
        menu.day_of_week: menu
        for menu in menus
    }

    days = []

    for number, name in DailyMenu.DAYS:
        days.append({
            "number": number,
            "name": name,
            "menu": menu_by_day.get(number),
        })

    return render(
        request,
        "menu/daily_menu.html",
        {
            "days": days,
        }
    )


@staff_required
def manage_daily_meal(request, day_of_week):
    if day_of_week < 0 or day_of_week > 4:
        messages.error(request, "Invalid day selected.")
        return redirect("daily_menu")

    menu, created = DailyMenu.objects.get_or_create(
        day_of_week=day_of_week
    )

    if request.method != "POST":
        return redirect("daily_menu")

    action = request.POST.get("action")
    name = request.POST.get("name", "").strip()

    # ADD FOOD
    if action == "add_food":
        if not name:
            messages.error(request, "Please enter a food name.")
            return redirect("daily_menu")

        food, created = Food.objects.get_or_create(
            name=name,
            defaults={
                "is_active": True
            }
        )

        if not food.is_active:
            food.is_active = True
            food.save(update_fields=["is_active"])

        menu.foods.add(food)

        messages.success(
            request,
            f"{food.name} added to {menu.get_day_of_week_display()}."
        )

    # DELETE FOOD FROM THIS DAY
    elif action == "delete_food":
        food_id = request.POST.get("food_id")

        food = get_object_or_404(
            Food,
            id=food_id
        )

        menu.foods.remove(food)

        messages.success(
            request,
            f"{food.name} removed from {menu.get_day_of_week_display()}."
        )

    # ADD SIDE
    elif action == "add_side":
        if not name:
            messages.error(request, "Please enter a side name.")
            return redirect("daily_menu")

        side, created = Vegetable.objects.get_or_create(
            name=name,
            defaults={
                "is_active": True
            }
        )

        if not side.is_active:
            side.is_active = True
            side.save(update_fields=["is_active"])

        menu.vegetables.add(side)

        messages.success(
            request,
            f"{side.name} added to {menu.get_day_of_week_display()}."
        )

    # DELETE SIDE FROM THIS DAY
    elif action == "delete_side":
        side_id = request.POST.get("side_id")

        side = get_object_or_404(
            Vegetable,
            id=side_id
        )

        menu.vegetables.remove(side)

        messages.success(
            request,
            f"{side.name} removed from {menu.get_day_of_week_display()}."
        )

    else:
        messages.error(request, "Invalid action.")

    return redirect("daily_menu")


# Existing Foods & Sides management
@staff_required
def foods_sides(request):
    foods = Food.objects.all()
    vegetables = Vegetable.objects.all()

    return render(
        request,
        "menu/foods_sides.html",
        {
            "foods": foods,
            "vegetables": vegetables,
        }
    )


@staff_required
def add_food(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            Food.objects.create(name=name)
            messages.success(request, "Food added successfully.")

    return redirect("foods_sides")


@staff_required
def add_side(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            Vegetable.objects.create(name=name)
            messages.success(request, "Side added successfully.")

    return redirect("foods_sides")


@staff_required
def delete_food(request, food_id):
    if request.method == "POST":
        food = get_object_or_404(Food, id=food_id)
        food.delete()

        messages.success(
            request,
            "Food deleted successfully."
        )

    return redirect("foods_sides")


@staff_required
def delete_side(request, vegetable_id):
    if request.method == "POST":
        side = get_object_or_404(
            Vegetable,
            id=vegetable_id
        )
        side.delete()

        messages.success(
            request,
            "Side deleted successfully."
        )

    return redirect("foods_sides")


@staff_required
def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == "POST":
        food.name = request.POST.get("name", "").strip()
        food.description = request.POST.get("description", "").strip()
        food.is_active = "is_active" in request.POST
        food.save()

        messages.success(
            request,
            "Food updated successfully."
        )

    return redirect("foods_sides")


@staff_required
def edit_side(request, vegetable_id):
    side = get_object_or_404(
        Vegetable,
        id=vegetable_id
    )

    if request.method == "POST":
        side.name = request.POST.get("name", "").strip()
        side.is_active = "is_active" in request.POST
        side.save()

        messages.success(
            request,
            "Side updated successfully."
        )

    return redirect("foods_sides")


@staff_required
def edit_daily_menu(request, day_of_week):
    if day_of_week < 0 or day_of_week > 4:
        messages.error(request, "Invalid day selected.")
        return redirect("daily_menu")

    menu, created = DailyMenu.objects.get_or_create(
        day_of_week=day_of_week
    )

    if request.method == "POST":
        menu.foods.set(
            request.POST.getlist("foods")
        )

        menu.vegetables.set(
            request.POST.getlist("vegetables")
        )

        menu.is_active = "is_active" in request.POST
        menu.save()

        messages.success(
            request,
            f"{menu.get_day_of_week_display()} menu updated successfully."
        )

        return redirect("daily_menu")

    foods = Food.objects.filter(is_active=True)
    vegetables = Vegetable.objects.filter(is_active=True)

    return render(
        request,
        "menu/edit_daily_menu.html",
        {
            "menu": menu,
            "foods": foods,
            "vegetables": vegetables,
            "day_name": menu.get_day_of_week_display(),
        }
    )
