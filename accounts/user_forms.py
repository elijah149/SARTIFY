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

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "is_active",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

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

    class Meta:
        model = User
        fields = [
            "username",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": "Leave empty to keep current password"
                }
            ),
            required=False
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
