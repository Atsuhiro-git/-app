from django import forms
from .models import Contact

#マイページフォーム
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['title', 'email' , 'content']
        labels = {
           'title':'題目',
           'email': 'メールアドレス',
           'content':'内容',
        }