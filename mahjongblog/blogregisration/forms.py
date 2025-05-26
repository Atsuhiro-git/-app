# blog/forms.py
from django import forms
from .models import Post, Category
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import bleach
from bleach.css_sanitizer import CSSSanitizer

#記事本文作成フォーム
class HTMLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    # ここで.clean()内にstyles引数を入れるとエラー(bleachではすでにstyle引数は廃止されている)
    def to_python(self, value):
        value       = super(HTMLField, self).to_python(value)
        return bleach.clean(value, tags=settings.ALLOWED_TAGS, attributes=settings.ATTRIBUTES, css_sanitizer=CSSSanitizer())

#記事フォーム
class PostForm(forms.ModelForm):
    # このカテゴリーに属さない投稿を複数選択できるフィールドを追加
    add_posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
        label='このカテゴリーに追加する投稿'
    )

    content = HTMLField()
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'タイトル'}),
            'tag': forms.Select(attrs={'class': 'form-select'}),
            'category' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'カテゴリー'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '本文'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                # このカテゴリーに属さない投稿を選択肢に設定
                self.fields['add_posts'].queryset = Post.objects.exclude(category=self.instance)
            else:
                self.fields['add_posts'].queryset = Post.objects.all()
    

#カテゴリーフォーム       
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']  # 'name'のみは元々のフィールド

#カテゴリー名フォーム        
class CategoryNameForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'カテゴリー名',
        }

#投稿のトップ画像フォーム
class PostImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']  # 画像だけ


