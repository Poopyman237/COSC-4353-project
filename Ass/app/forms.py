from django import forms

from app.models import Profile, FuelQuote


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_Name', 'address_1', 'address_2', 'city', 'state', 'zipcode']


class FuelQuoteForm(forms.ModelForm):
    class Meta:
        model = FuelQuote
        fields = ['gallons_requested', 'delivery_address', 'delivery_date', 'rate', 'user']
        widgets = {
            'delivery_date': forms.DateInput(format=('%m/%d/%Y'),
                                            attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }

    # def __init__(self, *arg, **kwargs):
    #     super().__init__(*arg, **kwargs)
    #     self.fields['']
