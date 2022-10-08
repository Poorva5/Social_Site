from django.urls import path
from .views import login_view, registration_view, logout_view, ProfileView, AddFollower, RemoveFollower


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path("<phone>/", ProfileView.as_view(), name="profile_page"),
    path('profile/<phone>/followers/add', AddFollower.as_view(), name='add_follower'),
    path('profile/<phone>/followers/remove', RemoveFollower.as_view(), name='remove_follower'),
]