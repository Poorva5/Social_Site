from django import forms
from .models import UserData, PostData
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


class PostDataForm(forms.ModelForm):
    class Meta:
        model = PostData
        fields = ('title', 'image', 'content')

    def __init__(self, *args, **kwargs):
        super(PostDataForm, self).__init__(*args, **kwargs)
        for field in (self.fields['title'], self.fields['content'], self.fields['image']):
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = PostData
        fields = ['title', 'image', 'content']

    def save(self, commit=False):
        posts = self.instance
        posts.title = self.cleaned_data['title']
        posts.content = self.cleaned_data['content']

        if self.cleaned_data['image']:
            posts.image = self.cleaned_data['image']
        if commit:
            posts.save()
        return posts

    def __init__(self, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        for field in (self.fields['title'], self.fields['content']):
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class SearchForm(forms.Form):
    query = forms.CharField()
