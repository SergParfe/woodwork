from django.db.models import Prefetch
from django.shortcuts import render

from works.models import Comment, Content, Image, Work
from works.utils import language_tool


def index(request, language='eng'):
    language, context = language_tool(language, request)
    template = f'works/{language}/index.html'

    works = (
        Work.objects.all()
        .prefetch_related(
            Prefetch(
                'comment',
                queryset=Comment.is_approved.all(),
                to_attr='comment_unit',
            ),
            Prefetch(
                'content',
                queryset=Content.objects.filter(language=language),
                to_attr='content_unit',
            ),
            Prefetch(
                'images',
                queryset=Image.objects.filter(order=0),
                to_attr='main_image',
            ),
        )
        .select_related('author')
        .order_by('?')[:6]
    )
    context |= {'works': works}
    return render(request, template, context)
