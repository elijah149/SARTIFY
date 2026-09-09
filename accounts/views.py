from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from menu.models import DailyMenu, Food, Vegetable
from orders.models import Order


@login_required
def dashboard(request):
    today = date.today()

    # Get Monday of the current week
    monday = today - timedelta(days=today.weekday())

    # Load all weekday menus with their foods and sides
    menus = (
        DailyMenu.objects
        .filter(
            day_of_week__range=(0, 4),
            is_active=True,
        )
        .prefetch_related(
            "foods",
            "vegetables",
        )
    )

    menu_by_day = {
        menu.day_of_week: menu
        for menu in menus
    }

    # Only active orders for the current Monday-Friday week
    active_orders = (
        Order.objects
        .filter(
            user=request.user,
            order_date__range=(
                monday,
                monday + timedelta(days=4),
            ),
            status__in=[
                "pending",
                "confirmed",
                "completed",
            ],
        )
        .select_related(
            "food",
            "vegetable",
        )
        .order_by(
            "order_date",
            "-created_at",
        )
    )

    ordered_dates = {
        order.order_date
        for order in active_orders
    }

    days = []

    for number, name in DailyMenu.DAYS:
        current_date = monday + timedelta(days=number)

        menu = menu_by_day.get(number)

        days.append({
            "number": number,
            "name": name,
            "date": current_date,
            "menu": menu,
            "already_ordered": current_date in ordered_dates,
        })

    return render(
        request,
        "accounts/dashboard.html",
        {
            "days": days,
            "week_orders": active_orders,
            "monday": monday,
            "friday": monday + timedelta(days=4),
        },
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return render(
            request,
            "accounts/access_denied.html",
        )

    total_users = User.objects.filter(
        is_staff=False
    ).count()

    total_foods = Food.objects.filter(
        is_active=True
    ).count()

    total_vegetables = Vegetable.objects.filter(
        is_active=True
    ).count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    total_orders = Order.objects.count()

    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "total_users": total_users,
            "total_foods": total_foods,
            "total_vegetables": total_vegetables,
            "pending_orders": pending_orders,
            "total_orders": total_orders,
        },
    )
