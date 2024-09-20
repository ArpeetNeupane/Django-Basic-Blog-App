from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) #required = True is default no need to write
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Date picker for birthday

    class Meta: #class meta gives us a nested namespace for configurations and keeps the configurations in one place
        model = User #the model that will be affected is the user model, eg: if we save(), it will save it to User
        fields = ['username', 'email', 'birthday', 'password1', 'password2'] #field we want in formT and in what order


#for updating user information in profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'birthday']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']