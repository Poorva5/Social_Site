from django.urls import path
from .views import home, login_view, registration_view, logout_view, create_post, post_detail, update_post, post_delete


urlpatterns = [
   path('home/', home, name="home"),
   path('login/', login_view, name='login'),
   path('register/', registration_view, name='signup'),
   path('logout/', logout_view, name='logout'),
   path('createpost/', create_post, name='create_post'),
   path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name="post_detail"),
   path('update/<slug>', update_post, name='update_post'),
   path('delete/<str:slug>', post_delete.as_view(), name="post_delete")
]