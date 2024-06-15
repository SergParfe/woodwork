from django.forms import ModelForm

from works.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
