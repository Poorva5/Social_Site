from django.urls import path
from .views import home, login_view, registration_view, logout_view


urlpatterns = [
   path('home/', home, name="home"),
   path('login/', login_view, name='login'),
   path('register/', registration_view, name='signup'),
   path('logout/', logout_view, name='logout')

]