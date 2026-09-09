from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "food",
            "vegetable",
            "quantity",
            "special_request",
        ]

        widgets = {
            "food": forms.Select(),
            "vegetable": forms.Select(),
            "quantity": forms.NumberInput(
                attrs={
                    "min": 1,
                    "value": 1,
                }
            ),
            "special_request": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Optional special request",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        daily_menu = kwargs.pop("daily_menu", None)

        super().__init__(*args, **kwargs)

        if daily_menu:
            self.fields["food"].queryset = daily_menu.foods.filter(
                is_active=True
            )

            self.fields["vegetable"].queryset = daily_menu.vegetables.filter(
                is_active=True
            )

        self.fields["vegetable"].required = False
