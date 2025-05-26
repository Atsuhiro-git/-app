# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CategoryForm, CategoryNameForm, PostImageForm
from .models import Post, Category
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators  import  login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def post_create(request, user_id):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # 確定ボタン押下（画像含むフォームでPOST）

            post_data = request.session.get('post_data')
            if not post_data:
                return redirect('post_create', user_id=user_id)

            post_form = PostForm(post_data)
            image_form = PostImageForm(request.POST, request.FILES)

            if post_form.is_valid() and image_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.image = image_form.cleaned_data['image']
                post.save()

                # セッションをクリア
                request.session.pop('post_data', None)

                return redirect('user_post_list', user_id=request.user.id)
            else:
                # フォームエラー時は投稿フォームに戻すなど対応
                return render(request, 'templates/blogregisration/post_form.html', {'form': post_form})

        else:
            # 初回投稿フォーム送信（画像なし）

            post_form = PostForm(request.POST)
            if post_form.is_valid():
                # フォームのPOSTデータをセッション保存
                request.session['post_data'] = request.POST

                # 確認画面へ画像アップロードフォームを渡す
                image_form = PostImageForm()
                return render(request, 'templates/blogregisration/post_confirm.html', {
                    'post_form': post_form,
                    'image_form': image_form,
                })

    else:
        post_form = PostForm()

    return render(request, 'templates/blogregisration/post_form.html', {'form': post_form})

#投稿記事の詳細
@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        post.delete()
        return redirect('user_post_list', user_id=request.user.id)  # 削除後は投稿一覧にリダイレクト

    return render(request, 'templates/blogregisration/post_confirm_delete.html', {'post': post})

#投稿記事一覧
@login_required
def post_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_uuid = request.user.id

    if user != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    # ユーザーの投稿をカテゴリー有無で分けて取得
    posts_with_category = Post.objects.filter(author=user, category__isnull=False).order_by('-created_at')
    posts_without_category = Post.objects.filter(author=user, category__isnull=True).order_by('-created_at')

    categories = Category.objects.all().prefetch_related('posts')
    

    return render(request, 'templates/blogregisration/all_views.html', {
        'categories': categories,
        'posts_with_category': posts_with_category,
        'posts_without_category': posts_without_category,
        'user_uuid' : user_uuid,
    })

#投稿物の編集
@login_required
def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_category = post.category
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # カテゴリーがPOSTデータにない場合、既存カテゴリーをセットする
            if not form.cleaned_data.get('category'):
                form.instance.category = post_category
            form.save()
            return redirect('user_post_list', user_id=request.user.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'templates/blogregisration/post_form.html', {'form': form, 'title': '投稿編集'})

# カテゴリー作成
@login_required
def category_create(request,user_id):
    user = get_object_or_404(User, pk=user_id)

    if user != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    # ユーザーの投稿をカテゴリー有無で分けて取得
    posts_with_category = Post.objects.filter(author=user, category__isnull=False).order_by('-created_at')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            form.save()
            return redirect('category_list',user_id=request.user.id)
    else:
        form = CategoryForm()
    return render(request, 'templates/blogregisration/category_form.html', {
        'form': form, 
        'title': 'カテゴリー作成',
        'posts_with_category' : posts_with_category
        })

#カテゴリーの消去
@login_required
def category_delete(request, category_number_id, user_id):
    category = get_object_or_404(Category, number=category_number_id)
    print(category.author)
    
    # 削除権限チェック（必要に応じて）
    if category.author != request.user:
        print(request.method)
        messages.error(request, "このカテゴリーを削除する権限がありません。")
        return redirect('category_list', user_id=request.user.id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, f'カテゴリー「{category.name}」を削除しました。')
        return redirect('category_list', user_id=request.user.id)

    # GETリクエストはリダイレクトかエラーページにするのが一般的です
    return redirect('category_list', user_id=request.user.id)


# カテゴリー編集
@login_required
def category_edit(request, category_number_id, user_id):
    category = get_object_or_404(Category, pk=category_number_id)
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST' and "save_category" in request.POST:
        # カテゴリー名の保存処理
        form = PostForm(request.POST, instance=category)
        return redirect('category_list', user_id=request.user.id)
    else:
        form = PostForm(instance=category)
    
    posts_with_category = Post.objects.filter(author=user, category__isnull=False).order_by('-created_at')
    posts_without_category = Post.objects.filter(author=user, category__isnull=True).order_by('-created_at')

    return render(request, 'templates/blogregisration/category_edit.html', {
        'category': category,
        'posts_in': posts_with_category,
        'posts_out': posts_without_category,
        'form': form,
    })

#カテゴリーに記事を追加
@require_POST
def category_add_post(request, category_number_id, user_id, post_pk):
    print('aa')
    category = get_object_or_404(Category, pk=category_number_id)
    user = get_object_or_404(User, pk=user_id)
    post_id = request.POST.get('post_id')
    if not post_id:
        return JsonResponse({'success': False, 'error': 'post_id is required'})
    try:
        post = Post.objects.get(author=user, category__isnull=True,id=post_pk)
        print(post)
        post.category = category
        post.save()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'post not found'})

#カテゴリーから記事を消去
@require_POST
def category_remove_post(request, category_number_id, user_id,post_pk):
    post_id = request.POST.get('post_id')
    user = get_object_or_404(User, pk=user_id)
    if not post_id:
        return JsonResponse({'success': False, 'error': 'post_id is required'})
    try:
        post = Post.objects.get(author=user, category__isnull=False, id=post_pk)
        post.category = None
        post.save()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'post not found or not in category'})

# カテゴリー一覧
@login_required
def category_list(request,user_id):
    user = get_object_or_404(User, pk=user_id)

    if user != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    # ユーザーの投稿をカテゴリー有無で分けて取得
    posts_with_category = Post.objects.filter(author=user, category__isnull=False).order_by('-created_at')
    categories = Category.objects.filter(author=user)
    
    return render(request, 'templates/blogregisration/category_list.html', {
        'posts_with_category': posts_with_category,
        'categories' : categories
        })

#カテゴリー名の編集
@login_required
def category_name_edit(request, category_number_id, user_id):
    category = get_object_or_404(Category, pk=category_number_id)

    if request.method == 'POST':
        form = CategoryNameForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list', user_id=request.user.id)  # 適宜リダイレクト先を変更
    else:
        form = CategoryNameForm(instance=category)

    return render(request, 'templates/blogregisration/category_name_edit.html', {
        'form': form,
        'category': category,
    })