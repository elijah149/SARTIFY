from django import forms

from .models import Food, Vegetable, DailyMenu


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter food name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Optional description"
                }
            ),
        }


class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ["name", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter side name"}
            ),
        }


class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ["foods", "vegetables", "is_active"]
        widgets = {
            "foods": forms.CheckboxSelectMultiple(),
            "vegetables": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["foods"].queryset = Food.objects.filter(
            is_active=True
        )

        self.fields["vegetables"].queryset = Vegetable.objects.filter(
            is_active=True
        )

        self.fields["foods"].required = False
        self.fields["vegetables"].required = False
