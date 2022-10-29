from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']

    def clean_text(self):
        return self.cleaned_data['text']
