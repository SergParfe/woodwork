from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Name')
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
    lang = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        blank=False,
        unique=True,
        verbose_name='Язык',
        default=ENG,
    )

    class Meta:
        verbose_name = 'Текст статьи'
        verbose_name_plural = 'Тексты статей'

    def __str__(self):
        return self.title[:25]


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
    content = models.ManyToManyField(
        Content,
        related_name='texts_of_project',
        verbose_name='Тексты статьи',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return Content.objects.get(
            texts_of_project__id=self.pk, lang='eng'
        ).title
