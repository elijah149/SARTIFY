from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from menu.models import DailyMenu

from .forms import OrderForm
from .models import Order


@login_required
def create_order(request, day_of_week):

    if day_of_week < 0 or day_of_week > 4:
        messages.error(
            request,
            "Orders are available from Monday to Friday only."
        )
        return redirect("dashboard")

    daily_menu = DailyMenu.objects.filter(
        day_of_week=day_of_week,
        is_active=True
    ).prefetch_related(
        "foods",
        "vegetables"
    ).first()

    if not daily_menu:
        messages.error(
            request,
            "No menu is available for this day."
        )
        return redirect("dashboard")

    # Current week's Monday
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    # Actual date for selected day
    order_date = monday + timedelta(days=day_of_week)

    # Check if user already has an active order for this day
    existing_order = Order.objects.filter(
        user=request.user,
        order_date=order_date,
        status__in=[
            "pending",
            "confirmed",
            "completed",
        ]
    ).first()

    if existing_order:
        messages.warning(
            request,
            f"You already have an order for "
            f"{daily_menu.get_day_of_week_display()}."
        )
        return redirect("dashboard")

    if request.method == "POST":

        form = OrderForm(
            request.POST,
            daily_menu=daily_menu
        )

        if form.is_valid():

            # Double-check before saving
            existing_order = Order.objects.filter(
                user=request.user,
                order_date=order_date,
                status__in=[
                    "pending",
                    "confirmed",
                    "completed",
                ]
            ).first()

            if existing_order:
                messages.warning(
                    request,
                    "You already have an order for this day."
                )
                return redirect("dashboard")

            order = form.save(commit=False)

            order.user = request.user
            order.order_date = order_date
            order.status = "pending"

            order.save()

            messages.success(
                request,
                f"Order placed successfully for "
                f"{daily_menu.get_day_of_week_display()}."
            )

            return redirect("dashboard")

    else:

        form = OrderForm(
            daily_menu=daily_menu
        )

    return render(
        request,
        "orders/create_order.html",
        {
            "form": form,
            "daily_menu": daily_menu,
            "order_date": order_date,
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user,
        status__in=[
            "pending",
            "confirmed",
            "completed",
        ]
    ).select_related(
        "food",
        "vegetable"
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
        }
    )


@login_required
def cancel_order(request, order_id):

    order = Order.objects.filter(
        id=order_id,
        user=request.user
    ).first()

    if not order:
        messages.error(
            request,
            "Order not found."
        )
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("dashboard")

    if order.status == "pending":

        order.status = "cancelled"

        order.save(
            update_fields=["status"]
        )

        messages.success(
            request,
            "Order cancelled successfully."
        )

    else:

        messages.error(
            request,
            "Only pending orders can be cancelled."
        )

    return redirect("dashboard")


@login_required
def admin_orders(request):

    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect("dashboard")

    today = date.today()

    monday = today - timedelta(
        days=today.weekday()
    )

    friday = monday + timedelta(days=4)

    orders = Order.objects.filter(
        order_date__range=(
            monday,
            friday
        )
    ).select_related(
        "user",
        "food",
        "vegetable"
    )

    user_data = {}

    for order in orders:

        username = order.user.username

        if username not in user_data:

            user_data[username] = {
                "username": username,
                "Monday": [],
                "Tuesday": [],
                "Wednesday": [],
                "Thursday": [],
                "Friday": [],
            }

        day_name = order.order_date.strftime("%A")

        meal = order.food.name

        if order.vegetable:
            meal += f" {order.vegetable.name}"

        user_data[username][day_name].append(meal)

    users = list(user_data.values())

    users.sort(
        key=lambda user: user["username"].lower()
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]

    return render(
        request,
        "orders/admin_orders.html",
        {
            "users": users,
            "days": days,
            "monday": monday,
            "friday": friday,
        }
    )
