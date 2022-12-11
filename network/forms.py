from dataclasses import field
from django import forms

from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'content',) 
        labels = {"comment": ""}

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'})
        }

