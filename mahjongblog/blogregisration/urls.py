# blog/urls.py
from django.urls import include, path
from . import views
import uuid
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:user_id>/create/', views.post_create, name='post_create'),
    path('<uuid:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:user_id>/views/', views.post_list, name='user_post_list'),  # ルートを一覧ページに
    path('<uuid:post_pk>/edit/', views.post_edit, name='post_edit'),
    path('summernote/', include('django_summernote.urls')),
    #カテゴリー作成・編集
    path('<int:user_id>/categories/', views.category_list, name='category_list'),
    path('<int:user_id>/categories/create/', views.category_create, name='category_create'),
    path('<int:user_id>/categories/<int:category_number_id>/delete/', views.category_delete, name='category_delete'),
    path('<int:user_id>/categories/<int:category_number_id>/edit/', views.category_edit, name='category_edit'),
    path('<int:user_id>/categories/<int:category_number_id>/<uuid:post_pk>/add_post/', views.category_add_post, name='category_add_post'),
    path('<int:user_id>/categories/<int:category_number_id>/<uuid:post_pk>/remove_post/', views.category_remove_post, name='category_remove_post'),
    path('<int:user_id>/categories/<int:category_number_id>/name_edit/', views.category_name_edit, name='category_name_edit'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

