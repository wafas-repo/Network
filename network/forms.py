from dataclasses import field
from django import forms
from django.forms import ModelForm

from .models import Post, UserProfile

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'content',) 
        labels = {"comment": " "}

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder':'What is on your mind...'})
        }

class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']
        

