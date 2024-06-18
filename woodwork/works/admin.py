from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from works.models import Comment, Content, Image, Tag, Work

admin.site.unregister(Group)


class ContentInline(admin.TabularInline):
    model = Work.content.through
    verbose_name = 'Текст проекта'
    verbose_name_plural = 'Тексты проекта'
    extra = 2
    min_number = 2


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('photo', 'image', 'description', 'order')
    verbose_name = 'Картинка'
    verbose_name_plural = 'Картинки'
    extra = 1
    min_number = 1
    ordering = ('order',)
    readonly_fields = ('photo',)

    @admin.display(description='Изображение')
    def photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=100>')


class CommentInline(admin.TabularInline):
    model = Work.comment.through
    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии'
    extra = 1
    min_number = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = list_display


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text'[:40],
    )
    search_fields = (
        'title',
        'text',
    )
    list_filter = ('title',)
    autocomplete_fields = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'approved',
        'project',
    )
    fields = (
        'author',
        'text',
        'approved',
        'pub_date',
    )
    readonly_fields = ('pub_date',)
    search_fields = (
        'title',
        'text',
    )
    list_filter = (
        'author',
        'approved',
    )
    list_editable = ('approved',)
    ordering = (
        'approved',
        '-pub_date',
    )

    def project(self, obj):
        return Content.objects.get(
            language='eng',
            content_to_work__id=Work.objects.get(comment=obj.pk).pk,
        ).title[:25]


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    fields = (
        ('slug', 'author'),
        ('made', 'pub_date'),
    )
    readonly_fields = ('pub_date',)
    save_on_top = True
    inlines = (
        ContentInline,
        ImageInline,
        CommentInline,
    )
    list_display = (
        'photo',
        'eng_title',
        'slug',
        'made',
    )
    list_display_links = list_display[:2]
    search_fields = (
        'content__title',
        'content__text',
    )
    list_filter = ('author',)

    @admin.display(description='Изображение')
    def photo(self, obj):
        images = Image.objects.filter(work=obj.pk)
        if images:
            return mark_safe(f'<img src="{images[0].image.url}" width=50>')
        return 'Без фото'

    @admin.display(description='Заголовок')
    def eng_title(self, obj):
        return Content.objects.get(
            language='eng', content_to_work__id=obj.pk
        ).title[:25]

    def get_form(self, request, obj=None, **kwargs):
        '''Задает значение поля author по умолчанию.'''
        form = super(WorkAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


@admin.register(Work.content.through)
class ContentsOfWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(Work.comment.through)
class CommentsOfWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = (
        'photo',
        'order',
        'description',
        'work',
        'image',
        'pub_date',
    )
    readonly_fields = (
        'photo',
        'pub_date',
    )
    list_display = (
        'photo',
        'image',
        'work',
        'order',
        'description',
    )
    list_display_links = (
        'photo',
        'work',
    )
    list_editable = ('order',)
    ordering = (
        '-work',
        'order',
    )

    @admin.display(description='Изображение')
    def photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=100>')
