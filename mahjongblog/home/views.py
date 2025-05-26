from django.shortcuts import render, redirect
from django.contrib.auth.decorators  import  login_required
import sys
from blogregisration.models import Post
from accounts.models import *
from django.shortcuts import render, get_object_or_404
from .forms import ContactForm
import random

# Topページ
def Top(request):
    # 人気記事
    popular_posts = Post.objects.order_by('-created_at')[:5]
    
    plofiles = CustomUser.objects.all()

    # タグ一覧
    TAG_CHOICES = dict(Post.TAG_CHOICES)  

    # タグ別人気記事（タグごとに5件ずつ取得）
    tag_popular_posts = {}
    for tag_key, tag_name in TAG_CHOICES.items():
        posts = Post.objects.filter(tag=tag_key).order_by('-created_at')[:5]
        tag_popular_posts[tag_key] = {
            'name': tag_name,
            'posts': posts,
        }

    # 通常の最新投稿（トップページで表示したい場合）
    posts = Post.objects.order_by('-created_at')[:10]

    context = {
        'popular_posts': popular_posts,
        'tag_popular_posts': tag_popular_posts,
        'posts': posts,
        'plofiles' : plofiles,
    }

    return render(request, 'templates/home/home_top.html', context)


#タグごとのページ
def tag_post_list(request, tag_key):
    TAG_CHOICES = dict(Post.TAG_CHOICES)
    tag_name = TAG_CHOICES.get(tag_key, '不明なタグ')
    posts = Post.objects.filter(tag=tag_key).order_by('-created_at')
    plofiles = CustomUser.objects.all()
    return render(request, 'templates/home/tag_post_list.html', {'tag_key': tag_key, 'tag_name': tag_name, 'posts': posts, 'plofiles': plofiles})

#マイページ
@login_required
def post_list(request):
    return render(request, 'templates/registration/post_list.html')

#記事詳細
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    # おすすめ記事のクエリセットを初期化
    recommended_posts = Post.objects.none()
    
    if post.category:
        # 同じカテゴリーの他の記事（自身は除く）
        qs = Post.objects.filter(category=post.category).exclude(pk=post.pk)
    else:
        # カテゴリーがなければ同じ作者の他の記事
        qs = Post.objects.filter(author=post.author).exclude(pk=post.pk)

    # ランダムに3件程度取得（件数は調整可）
    count = qs.count()
    if count <= 2:
        recommended_posts = qs
    else:
        # ランダム抽出
        pks = random.sample(list(qs.values_list('pk', flat=True)), 2)
        recommended_posts = Post.objects.filter(pk__in=pks)

    return render(request, 'templates/home/post_detail.html', {
        'post': post,
        'recommended_posts': recommended_posts,
    })

def privacy_policy(request):
    return render(request, 'templates/home/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'templates/home/terms_of_service.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/top')
    else:
        form = ContactForm()
    return render(request, 'templates/home/contact.html',{'form':form})