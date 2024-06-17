from django.contrib.auth import get_user_model
from django.db import models

from works.constants import EXCLUDE_WORKS_FROM_LIST

User = get_user_model()


class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved=True)


class WorkList(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(slug__in=EXCLUDE_WORKS_FROM_LIST)


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Name',
    )
    slug = models.SlugField(
        unique=True,
        max_length=256,
        verbose_name='Tag slug',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Content(models.Model):
    ENG = 'eng'
    RUS = 'rus'

    LANGUAGE_CHOICES = [
        (ENG, 'English'),
        (RUS, 'Русский'),
    ]

    title = models.CharField(max_length=256, verbose_name='Заголовок статьи')
    text = models.TextField(verbose_name='Текст статьи')
    tags = models.ManyToManyField(
        Tag,
        related_name='works',
        verbose_name='Теги',
    )
    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        blank=False,
        verbose_name='Язык',
        default=ENG,
    )

    class Meta:
        verbose_name = 'Текст статьи'
        verbose_name_plural = 'Тексты статей'

    def __str__(self):
        return self.title[:25]


class Image(models.Model):
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Проект',
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Файл картинки',
    )
    description = models.TextField(verbose_name='Описание')
    order = models.IntegerField(verbose_name='Номер для сортировки')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = (
            '-work',
            'order',
        )
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.image.url


class Comment(models.Model):
    author = models.CharField(
        max_length=128,
        verbose_name='Имя комментатора',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=512,
    )
    approved = models.BooleanField(null=False, default=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )

    objects = models.Manager()
    is_approved = ApprovedManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} написал: {self.text[:25]}'


class Work(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='works',
        verbose_name='Автор',
    )
    slug = models.SlugField(
        unique=True,
        max_length=256,
        verbose_name='Слаг статьи',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    made = models.DateTimeField(
        verbose_name='Дата изготовления',
    )
    content = models.ManyToManyField(
        Content,
        related_name='content_to_work',
        verbose_name='Тексты статьи',
    )
    comment = models.ManyToManyField(
        Comment,
        related_name='comment_to_work',
        verbose_name='Комментарии',
    )

    objects = models.Manager()
    worklist = WorkList()

    class Meta:
        ordering = ('-made',)
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return Content.objects.get(
            content_to_work__id=self.pk, language='eng'
        ).title
