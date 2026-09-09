from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .user_forms import UserCreateForm, UserEditForm


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
def users_list(request):
    search = request.GET.get(
        "search",
        ""
    ).strip()

    users = User.objects.filter(
        is_staff=False
    ).order_by(
        "username"
    )

    if search:
        users = users.filter(
            Q(username__icontains=search)
        )

    return render(
        request,
        "accounts/users.html",
        {
            "users": users,
            "search": search,
        }
    )


@staff_required
def add_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "User created successfully."
            )

            return redirect("users_list")
    else:
        form = UserCreateForm()

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Add User",
        }
    )


@staff_required
def edit_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
        is_staff=False
    )

    if request.method == "POST":
        form = UserEditForm(
            request.POST,
            instance=user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "User updated successfully."
            )

            return redirect("users_list")
    else:
        form = UserEditForm(
            instance=user
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Edit User",
            "user_obj": user,
        }
    )


@staff_required
def delete_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
        is_staff=False
    )

    if request.method == "POST":
        username = user.username

        user.delete()

        messages.success(
            request,
            f"User {username} deleted successfully."
        )

    return redirect("users_list")
