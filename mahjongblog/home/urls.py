from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('top/', views.Top, name='home/home_redirect'),
    path('tag/<str:tag_key>/', views.tag_post_list, name='home/tag_post_list'),
    path('', views.post_list),
    path('posts/<uuid:post_pk>/', views.post_detail, name='home/blog_post_detail'),
    path('privacypolicy', views.privacy_policy, name='home/privacy_policy'),
    path('terms_of_service/', views.terms_of_service,name='home/terms_of_service'),
    path('contact/', views.contact,name='home/contact'),
]