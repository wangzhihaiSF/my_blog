from django.forms import ModelForm

from article.models import ArticlePost


class ArticlePostForm(ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body")

