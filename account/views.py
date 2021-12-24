from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostDataForm


def home(request):
    return render(request, "base.html", {})


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
            form=RegistrationForm()
            return render(request, 'account/register.html', {'form':form})
    else:
        form = RegistrationForm()
        return render(request, "account/register.html", {'form': form})


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        print("user authenticated")
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
            messages.error(request, "Please Correct Below Error")
    else:
        form = LoginForm()
        context['login_form'] = form
        return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect("home")


def create_post(request):
    if request.method == 'POST':
        form = PostDataForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)




