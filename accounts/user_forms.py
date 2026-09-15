from django import forms
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter initial password"
            }
        ),
        min_length=6
    )

    role = forms.ChoiceField(
        choices=[
            ("user", "Normal User"),
            ("admin", "Administrator"),
        ],
        initial="user"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "role",
            "is_active",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        role = self.cleaned_data["role"]

        if role == "admin":
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()

        return user


class UserEditForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Leave empty to keep current password"
            }
        ),
        required=False
    )

    role = forms.ChoiceField(
        choices=[
            ("user", "Normal User"),
            ("admin", "Administrator"),
        ]
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "role",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].initial = (
            "admin"
            if self.instance.is_staff
            else "user"
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        role = self.cleaned_data["role"]

        if role == "admin":
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()

        return user
