from django import forms
from .models import Post, Comment, User


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


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'groups']

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.changed_data:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if groups.count() > 1:
            raise forms.ValidationError("Užívateľ môže byť členom maximálne jednej skupiny.")
        return groups
