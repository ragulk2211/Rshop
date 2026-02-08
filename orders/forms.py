from django import forms
from .models import Address, Order


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone_number",
            "address_line1",
            "address_line2",
            "landmark",
            "city",
            "state",
            "pincode",
            "is_default",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 1"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 2 (Optional)"}),
            "landmark": forms.TextInput(attrs={"class": "form-control", "placeholder": "Landmark (Optional)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.Select(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "placeholder": "PIN Code"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_pincode(self):
        """Validate that PIN code is exactly 6 digits."""
        pincode = self.cleaned_data.get("pincode")
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("PIN code must be exactly 6 digits.")
        return pincode

    def clean_phone_number(self):
        """Validate that phone number is exactly 10 digits."""
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    def clean(self):
        """
        Prevent duplicate address for same user.
        This avoids IntegrityError from UNIQUE constraint.
        """
        cleaned_data = super().clean()

        # IMPORTANT: user is not inside the form fields, so view must pass it
        user = self.initial.get("user")

        address_line1 = cleaned_data.get("address_line1")
        address_line2 = cleaned_data.get("address_line2") or ""
        pincode = cleaned_data.get("pincode")

        if user and address_line1 and pincode:
            exists = Address.objects.filter(
                user=user,
                pincode=pincode,
                address_line1=address_line1,
                address_line2=address_line2,
            ).exists()

            if exists:
                raise forms.ValidationError("This address already exists.")

        return cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address", "status"]
        widgets = {
            "address": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
