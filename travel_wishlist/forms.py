from django import forms
from django.forms import DateInput

from .models import Place

# input forms
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

# for users entering notes photos and date visited
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date visited': DateInput()
        }
