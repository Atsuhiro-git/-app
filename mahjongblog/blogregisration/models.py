# blog/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)
    number = models.PositiveIntegerField(verbose_name='番号', unique=True, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def save(self, *args, **kwargs):
        if self.number is None:
            # 既存の最大numberを取得
            max_number = Category.objects.aggregate(models.Max('number'))['number__max']
            self.number = (max_number or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.name}"
    

    def __str__(self):
        return self.name

class Post(models.Model):
    TAG_CHOICES = [
        ('majan', '麻雀入門'),
        ('zadaku', '座学'),
        ('haifu', '牌譜検討'),
        ('other', 'その他'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField(verbose_name="本文")
    image = models.ImageField(upload_to='media', blank=True, null=True)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='other')
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts',
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title