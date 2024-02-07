from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self):
        super(PostForm, self).__init__()
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['content'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': '12'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self):
        super(CommentForm, self).__init__()
        self.fields['comment'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': '12'})
