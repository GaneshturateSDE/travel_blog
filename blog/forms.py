from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap input style
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }