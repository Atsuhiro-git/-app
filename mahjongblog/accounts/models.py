from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 追加フィールドだけ定義する
    icon = models.ImageField(upload_to='user_icons/', blank=True, null=True)
    profile_message = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.username