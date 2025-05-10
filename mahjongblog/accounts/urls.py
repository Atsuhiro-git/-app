from django.urls import path
from . import views
from .views import home, LoginView

urlpatterns = [
    path('signup/',views.signup_view, name='signup'),
    path('login/',LoginView,name='login'),
    path('home/',home,name='home'),
    path("logout/", views.logout_request, name= "logout"),
    path('profile/<int:user_id>/', views.account_detail, name='account_detail'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
]
