from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from accounts import views as account_views
from accounts import user_views
from accounts.login_views import RoleBasedLoginView
from menu import views as menu_views
from orders import views as order_views


urlpatterns = [

    # Root → Login
    path(
        "",
        RedirectView.as_view(
            pattern_name="login",
            permanent=False
        ),
        name="home",
    ),

    # Authentication
    path(
        "login/",
        RoleBasedLoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # User Dashboard
    path(
        "dashboard/",
        account_views.dashboard,
        name="dashboard",
    ),

    # Custom Admin Dashboard
    path(
        "admin-dashboard/",
        account_views.admin_dashboard,
        name="admin_dashboard",
    ),

    # Daily Meals
    path(
        "admin-dashboard/daily-menu/",
        menu_views.daily_menu,
        name="daily_menu",
    ),

    path(
        "admin-dashboard/daily-menu/manage/<int:day_of_week>/",
        menu_views.manage_daily_meal,
        name="manage_daily_meal",
    ),

    path(
        "admin-dashboard/daily-menu/edit/<int:day_of_week>/",
        menu_views.edit_daily_menu,
        name="edit_daily_menu",
    ),

    # Users
    path(
        "admin-dashboard/users/",
        user_views.users_list,
        name="users_list",
    ),

    path(
        "admin-dashboard/users/add/",
        user_views.add_user,
        name="add_user",
    ),

    path(
        "admin-dashboard/users/edit/<int:user_id>/",
        user_views.edit_user,
        name="edit_user",
    ),

    path(
        "admin-dashboard/users/delete/<int:user_id>/",
        user_views.delete_user,
        name="delete_user",
    ),

    # Orders
    path(
        "orders/create/<int:day_of_week>/",
        order_views.create_order,
        name="create_order",
    ),

    path(
        "orders/my-orders/",
        order_views.my_orders,
        name="my_orders",
    ),

    path(
        "orders/admin-orders/",
        order_views.admin_orders,
        name="admin_orders",
    ),

    path(
        "orders/cancel/<int:order_id>/",
        order_views.cancel_order,
        name="cancel_order",
    ),
]
