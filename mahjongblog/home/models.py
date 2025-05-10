from django.db import models

# Create your models here.
class Contact(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'contacts'