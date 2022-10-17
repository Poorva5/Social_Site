from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostDataForm
from django.contrib import messages
from .models import PostData
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect



def home(request):
    context = {}
    data = PostData.objects.all()
    context['posts'] = data
    return render(request, "base.html", context)


def create_post(request):
    form = PostDataForm()
    if request.method == 'POST':
        form = PostDataForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            messages.success(request,"Post was created successfully")
            return redirect("home")
        else:
            messages.success(request, "Please Correct Below Errors")
            print(form.errors)
            form = PostDataForm()
            return render(request, "post/create_post.html",  {'form': form})
    context = {'form': form}
    return render(request, "post/create_post.html", context)


def post_detail(request, year, month, day, post):
    item = get_object_or_404(PostData, slug=post)
    user = request.user
    context = {
        'item': item
    }
    return render(request, "post/post_detail.html", context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = PostData.objects.filter(
            Q(caption__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))


def post_list(request):
    obj = PostData.objects.all()
    query = ""
    context = {}
    if request.GET:
        query = request.GET.get('q', '')
        print(query)
        context['query'] = str(query)
    obj = sorted(get_blog_queryset(query), reverse=True)
    context['obj'] = obj

    return render(request, "base.html", context)


class post_delete(DeleteView):
    model = PostData
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy("home")
    success_message = "Post Deleted Successfully"


def like_posts(request, pk):
    post = get_object_or_404(PostData, id=request.POST.get('post_id'))
    if post.user_like.filter(id=request.user.id).exists():
        post.user_like.remove(request.user)
    else:
        post.user_like.add(request.user)
        
    return HttpResponseRedirect(reverse('home'))    

    





