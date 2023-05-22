from django import forms

from .models import Post, Author, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, label="Имя автора", required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Категория", required=True, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'kind', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()

    def save(self, commit=True):
        author_name = self.cleaned_data.get('author_name')
        categories = self.cleaned_data.get('category')
        author = self.cleaned_data.get('author')

        if author_name:
            author, _ = Author.objects.get_or_create(user__username=author_name)

        self.instance.author = author
        post = super().save(commit=False)

        if commit:
            post.save()
            for category in categories:
                post.category.add(category)

        return post

class DateInput(forms.DateInput):
    input_type = 'date'

class NewsSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Название')
    author_name = forms.CharField(required=False, label='Имя автора')
    date_after = forms.CharField(required=False, label='Позже указываемой даты', widget=DateInput)


