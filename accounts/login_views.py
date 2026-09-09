from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class RoleBasedLoginView(LoginView):

    def get_success_url(self):
        if self.request.user.is_staff:
            return "/admin-dashboard/"

        return "/dashboard/"
