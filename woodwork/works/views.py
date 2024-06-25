from datetime import datetime
from http import HTTPStatus

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from works.constants import LANGUAGE, MAIN_PAGE_WORKS_COUNT, SWITCH_TO_LABELS
from works.forms import CommentForm
from works.models import Comment, Content, Image, Work
from works.utils import language_tool, send_telegram_message


def index(request, language='eng'):
    if language not in LANGUAGE:
        return redirect(f'{reverse("index")}{LANGUAGE[0]}/')
    context = language_tool(language, request)
    template = f'works/{language}/index.html'

    works = (
        Work.worklist.filter(is_on_main_page=True)
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
                to_attr='image_content',
            ),
        )
        .order_by('?')[:MAIN_PAGE_WORKS_COUNT]
    )
    context |= {'works': works}
    return render(request, template, context)


def page_not_found(request, exception):
    context = {
        'language': LANGUAGE[0],
        'switch_to_label': SWITCH_TO_LABELS[LANGUAGE[1]],
        'switch_to_url': f'/{LANGUAGE[1]}/',
        'year': datetime.now().strftime('%Y'),
        'path': request.path,
    }
    return render(
        request,
        '404.html',
        context,
        status=HTTPStatus.NOT_FOUND,
    )


def server_error_page(request):
    context = {
        'language': LANGUAGE[0],
        'switch_to_label': SWITCH_TO_LABELS[LANGUAGE[1]],
        'switch_to_url': f'/{LANGUAGE[1]}/',
        'year': datetime.now().strftime('%Y'),
        'path': request.path,
    }
    return render(
        request,
        '500.html',
        context,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def work_list(request, language='eng'):
    context = language_tool(language, request)
    works = (
        Work.worklist.all()
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
                queryset=Image.objects.all(),
                to_attr='image_content',
            ),
        )
        .select_related('author')
    )
    context |= {'works': works}
    template = f'works/{language}/work_list.html'
    return render(request, template, context)


def work_detail(request, slug, language='eng'):
    context = language_tool(language, request)
    template = f'works/{language}/work_detail.html'
    work = get_object_or_404(
        Work.objects.prefetch_related(
            Prefetch(
                'content',
                queryset=Content.objects.filter(
                    language=language
                ).prefetch_related('tags'),
                to_attr='content_unit',
            ),
            Prefetch(
                'comment',
                queryset=Comment.is_approved.all(),
                to_attr='comment_unit',
            ),
            Prefetch(
                'images',
                queryset=Image.objects.all(),
                to_attr='image_content',
            ),
        ),
        slug=slug,
    )
    context |= {'work': work}
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save()
            work.comment.add(comment)
            context |= {
                'work': work,
                'slug': work.slug,
            }
            message_to_telegram = '\n'.join(
                [
                    'Новый коментарий на сайте\n',
                    f'Работа: {work.slug}',
                    f'Автор: {comment.author}',
                    f'Пишет: {comment.text}',
                ]
            )
            send_telegram_message(message_to_telegram)
            return render(request, 'works/thanks.html', context)
        context |= {'comment_form': form}
        return render(request, template, context)

    form = CommentForm()
    context |= {'comment_form': form}

    return render(request, template, context)


def about_this_site(request, language='eng'):
    context = language_tool(language, request)
    template = 'works/about.html'
    work = (
        Work.objects.filter(slug='about_this_site')
        .prefetch_related(
            Prefetch(
                'content',
                queryset=Content.objects.filter(language=language),
                to_attr='content_unit',
            ),
            Prefetch(
                'images',
                queryset=Image.objects.all().order_by('?'),
                to_attr='image_content',
            ),
        )
        .first()
    )
    context |= {'work': work}
    return render(request, template, context)
