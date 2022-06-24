from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.Textarea)
    description = forms.CharField(max_length=500, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['user_id', 'title', 'description']


class UserIDForm(forms.Form):
    user_id = forms.IntegerField()

    class Meta:
        fields = ['user_id']


class PostIDForm(forms.Form):
    post_id = forms.IntegerField()

    class Meta:
        fields = ['post_id']


class BodyForm(forms.Form):
    body = forms.CharField(max_length=500, widget=forms.Textarea, label="")

    class Meta:
        fields = ['body']


class TitleForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.Textarea, label="")

    class Meta:
        fields = ['title']
