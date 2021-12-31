from django.urls import path
from .views import (
   home, login_view, registration_view, logout_view,
   create_post, post_detail, update_post, post_delete,
   profile_page, friend_request, all_users, friends,
   send_friend_request, accept_friend_request, post_list, user_search)

urlpatterns = [
   path('home/', home, name="home"),
   path('login/', login_view, name='login'),
   path('register/', registration_view, name='signup'),
   path('logout/', logout_view, name='logout'),
   path('createpost/', create_post, name='create_post'),
   path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name="post_detail"),
   path('update/<slug>', update_post, name='update_post'),
   path('delete/<str:slug>', post_delete.as_view(), name="post_delete"),
   path("user/<phone>/", profile_page, name="profile"),
   path("friend_requests/", friend_request, name="friend_request"),
   path('all_users/', all_users, name="users"),
   path('friends/', friends, name="friends"),
   path('send_friend_request/<int:userId>/', send_friend_request, name="send_friend_request"),
   path('accept_friend_request/<int:requestID>/', accept_friend_request, name="accept_friend_request"),
   path("", post_list, name="post_list"),
   path('search/', user_search, name='search'),
]