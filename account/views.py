from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostDataForm, UpdatePostForm
from django.http import HttpResponseRedirect
from .models import PostData, UserData
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import reverse_lazy



def home(request):
    context = {}
    data = PostData.objects.all()
    context['post_list'] = data
    return render(request, "base.html", context)


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
    form = PostDataForm()
    if request.method == 'POST':
        form = PostDataForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            messages.success(request, "Post was created successfully")
            return redirect("home")
        else:
            messages.error(request, "Please Correct Below Errors")
            print(form.errors)
            form = PostDataForm()
            return render(request, "account/Create_Post.html", {'form': form})
    context = {'form': form}
    return render(request, "account/Create_Post.html", context)


def post_detail(request, year, month, day, post):
    item = get_object_or_404(PostData, slug=post)
    user = request.user
    context = {
        'item': item
    }
    return render(request, "account/post_detail.html", context)


@login_required
def update_post(request, slug):
    context = {}
    user = request.user
    post = get_object_or_404(PostData, slug=slug)
    if request.method == 'POST':
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            context['success_message'] = "update"
            post = item
            messages.success(request, "{} was updated".format(item.title))
            return HttpResponseRedirect(post.get_absolute_url())

    form = UpdatePostForm(initial={
            'title': post.title,
            'content': post.content,
            'image': post.image,
        }
    )
    context['form'] = form
    return render(request, "account/update_post.html", context)


class post_delete(DeleteView):
    model = PostData
    template_name = 'account/delete_post.html'
    success_url = reverse_lazy("home")
    success_message = "Post Deleted Successfully"


# def profile_page(request, phone):
#     context = {}
#     print(UserData.objects.all())
#
#     obj = UserData.objects.filter(phone=phone)
#     all_users = UserData.objects.all()
#     obj = obj[0]
#     con_users = obj.friends.all()
#     x = []
#     request = FriendRequest.objects.all()






