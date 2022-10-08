from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserData
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from post.models import PostData


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                phone=form.cleaned_data['phone'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
        else:
            print(request.POST, form.errors)
            form = RegistrationForm()
            return render(request, 'account/register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, "account/register.html", {'form': form})

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = LoginForm(request.POST)
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(phone=phone, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("home")
        else:
            print(request.POST, form.errors)
            return render(request, 'account/login.html', {'login_form': form})
    else:
        form = LoginForm()
        context['login_form'] = form
        return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("signup")


# def profile_page(request, phone):
#     context = {}
#     obj = UserData.objects.filter(phone=phone)
#     print(obj)
#     obj = obj[0]
#     context = {
#         "obj": obj
#     }
#     return render(request, 'account/my_profile.html', context)


class ProfileView(View):
    
    def get(self, request, phone, *args, **kwargs):
        profile = UserData.objects.get(phone=phone)
        followers = request.user.followers.all()

        is_following = False
        if request.user in followers:
            is_following = True
            
        number_of_followers = len(followers)

        context = {
            'profile' : profile,
            'is_following' : is_following,
            'number_of_followers' : number_of_followers,
        }
        return render(request, 'account/my_profile.html', context)

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, phone, *args, **kwargs):
        profile = UserData.objects.get(phone=phone)
        profile.followers.add(request.user)
        return redirect('profile_page', phone=profile.phone)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, phone, *args, **kwargs):
        profile = UserData.objects.get(phone=phone)
        profile.followers.remove(request.user)

        return redirect('profile_page', phone=profile.phone)