from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        labels = {"text": "Текст", "group": "Группа"}
        fields = ['text', 'group']

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 5000:
            raise forms.ValidationError('Превышен предел символов')
        return text
