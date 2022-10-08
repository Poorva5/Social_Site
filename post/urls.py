from django.urls import path
from .views import create_post, post_detail, home, post_list, post_delete, like_posts

urlpatterns = [
    path('home/', home, name="home"),
    path('createpost/', create_post, name='create_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name="post_detail"),
    path("", post_list, name="post_list"),
    path('delete/<str:slug>', post_delete.as_view(), name="post_delete"),
    path('like/<int:pk>/', like_posts, name='like_post'),
]