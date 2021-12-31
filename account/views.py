from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostDataForm, UpdatePostForm , SearchForm
from django.http import HttpResponseRedirect
from .models import PostData, UserData, FriendRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from operator import attrgetter
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView




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
    return render(request, "account/logout.html")


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
            context['success_message'] = "updated"
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


@login_required
def profile_page(request, phone):
    context = {}
    print(UserData.objects.all())

    obj = UserData.objects.filter(phone=phone)
    all_users = UserData.objects.all()
    obj = obj[0]
    con_users = obj.friends.all()
    x = []
    requests = FriendRequest.objects.filter(to_user=request.user)
    for i in range(len(con_users)):
        mutual = []
        for j in con_users[i].friends.all():

            if con_users[i].friends.all() & request.user.friends.all():
                mutual.append(con_users[i].friends.all() & request.user.friends.all())
        x.append(mutual)
    context = {
        "requests": requests,
        "con_users": con_users,
        "obj": obj,
        "all_users": all_users
    }
    return render(request, 'account/profile.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = PostData.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))


def friend_request(request):
    user = request.user
    obj = FriendRequest.objects.filter(to_user=user)
    print(obj)
    context = {}
    context['frnd_requests']=obj
    return render(request, 'account/friend_requests.html', context)


def friends(request):
    user = request.user
    obj = user.friends.all()
    print(obj)
    context = {}
    context['friend'] = obj
    return render(request, "account/friends.html", context)


def all_users(request):
    obj = UserData.objects.exclude(user=request.user)
    context = {
        'users': obj
    }
    return render(request, 'account/users.html', context)


def send_friend_request(request, userId):
    from_user = request.user
    to_user = UserData.objects.get(id=userId)
    if from_user.phone == to_user.phone:
        messages.success(request, "Cannot send friend request to YOurself")
        return redirect("profile", phone=request.user.phone)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        messages.success(request, 'Friend Request Sent')
        return redirect("profile", phone=request.user.phone)
    else:
        messages.error(request, 'Friend Request was Already Sent')
        return redirect("profile", phone=request.user.phone)


def accept_friend_request(request, requestID):
     friend_request = FriendRequest.objects.get(id=requestID)
     if friend_request.to_user == request.user:
         friend_request.to_user.friends.add(friend_request.from_user)
         friend_request.from_user.friends.add(friend_request.to_user)
         friend_request.delete()
         messages.success(request, "Friend Request Accepted")
         return redirect("profile", phone=request.user.phone)
     else:
         messages.error(request, "Friend Request Not Accepted")
         return redirect("profile", phone=request.user.phone)


def post_list(request):
    obj = PostData.objects.all()
    query = ""
    context = {}
    if request.GET:
        query = request.GET.get('q', '')
        print(query)
        context['query'] = str(query)
    obj = sorted(get_blog_queryset(query), key=attrgetter('updated'), reverse=True)
    context['obj'] = obj

    return render(request, "base.html", context)


def user_search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        print(q)
        data = UserData.objects.filter(Q(name__icontains=q)| Q(phone__icontains=q)| Q(email__icontains=q))
    else:
        data = UserData.objects.all()
    context = {
        'data': data
    }
    return render(request, 'account/search.html', context)



def my_post_list(request):
    context = {}
    user = UserData.objects.all()
    data = PostData.objects.filter(author=user)
    context['post_list'] = data
    return render(request, "account/profile.html", context)



