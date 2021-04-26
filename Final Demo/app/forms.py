from django import forms

from app.models import Profile, FuelQuote


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_Name', 'address_1', 'address_2', 'city', 'state', 'zipcode']
        widgets = {
            'zipcode': forms.NumberInput(attrs={
                'required': True, 'min': 9999, 'max': 999999999,
                'maxlength': 9,
                'oninput': 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);'
                }),
            'full_name': forms.TextInput(attrs={'maxlength': 50}),
            'address_1': forms.TextInput(attrs={'maxlength': 100}),
            'address_2': forms.TextInput(attrs={'maxlength': 100}),
            'city': forms.TextInput(attrs={'maxlength': 100}),
        }


class FuelQuoteForm(forms.ModelForm):
    class Meta:
        model = FuelQuote
        fields = ['gallons_requested', 'delivery_address', 'delivery_date', 'rate']
        widgets = {
            'delivery_date': forms.DateInput(format=('%m/%d/%Y'),
                                            attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'rate': forms.NumberInput(attrs={'readonly': True})
        }

    # def __init__(self, *arg, **kwargs):
    #     super().__init__(*arg, **kwargs)
    #     self.fields['']