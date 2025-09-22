from django import forms
from django.contrib.auth.forms import UserCreationForm
from django .contrib.auth.models import User

from .models import Article, Comment

class AritcleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', ]
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
            
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
