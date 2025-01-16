from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']
        
        
    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class DateInput(forms.DateInput):
    input_type = 'date'
        
        
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'due', 'is_completed']
        widgets = {
            'due': DateInput()
        }
        
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        
'''class DashboardFom(forms.Form):
    text = forms.CharField(max_length=100, label='Enter your search : ')'''
    
class DashboardFom(forms.Form):
    text = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search Here'}))
    def __init__(self, *args, **kwargs):
        super(DashboardFom, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_completed']
        
    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        
        
class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    

class ConversionLengthForm(forms.Form):
    CHOICES = [('inch', 'Inch'), ('foot', 'Foot'), ('yard', 'Yard')]
    input = forms.CharField(required=False, label= False, widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter value'}))
    measure1 = forms.ChoiceField(choices=CHOICES, widget=forms.Select)
    measure2 = forms.ChoiceField(choices=CHOICES, widget=forms.Select)
    

class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False, label= False, widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter value'}))
    measure1 = forms.ChoiceField(choices=CHOICES, widget=forms.Select)
    measure2 = forms.ChoiceField(choices=CHOICES, widget=forms.Select)
    
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] 
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})