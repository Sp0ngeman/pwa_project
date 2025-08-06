from django import forms
from .models import Category

class NewTaskForm(forms.Form):
    task = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'id': 'task',
            'placeholder': 'New Task'
        })
    )
    # New field for category selection
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), # Populates choices from all Category objects
        required=False, # Category selection is optional
        widget=forms.Select(attrs={'id': 'category'}), # Renders as a select dropdown
        label="Category" # Label for the field
    ) 