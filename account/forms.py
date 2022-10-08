from django import forms
from .models import UserData
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model = UserData
        fields = ['phone', 'email', 'name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['phone'], self.fields['email'], self.fields['name'],
                      self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserData
        fields = ('phone', 'password')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in (self.fields['phone'], self.fields['password']):
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        if self.is_valid():
            phone = self.cleaned_data.get('phone')
            password = self.cleaned_data.get('password')
            if not authenticate(phone=phone, password=password):
                raise forms.ValidationError('Invalid Login')


