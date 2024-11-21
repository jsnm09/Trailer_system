# authentication/forms.py

from django import forms
from .models import Trailer  # Import the Trailer model

class TrailerForm(forms.ModelForm):
# Define choices for the status field
    STATUS_CHOICES = [
        ('', 'Select'),  # Placeholder option
        ('In Yard', 'In Yard'),
        ('In Transit', 'In Transit'),
        ('Available', 'Available'),
        ('Rented', 'Rented'),
    ]

    # Override the status field to use choices
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Status')

    class Meta:
        model = Trailer
        fields = ['name', 'status', 'rented_by', 'rent_due']

        widgets = {
            'rent_due': forms.DateInput(
                attrs={
                    'type': 'date',  # HTML5 date picker
                    'placeholder': 'YYYY-MM-DD',  # Example format
                    'title': 'Enter the date in YYYY-MM-DD format'  # Tooltip for additional guidance
                }
            ),
        }
