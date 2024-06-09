from django.contrib import admin
from works.models import Content, Tag, Work


class ContentInline(admin.TabularInline):
    model = Work.content.through
    verbose_name = 'Текст проекта'
    verbose_name_plural = 'Тексты проекта'
    extra = 0
    min_number = 2


"""
    Выглядит красиво, но не функционально
    
    fields = ('content_lang', 'content_title', 'content_text')
    readonly_fields = fields
    def content_title(self, obj):
        return Content.objects.get(pk=obj.content.pk).title

    def content_text(self, obj):
        return Content.objects.get(pk=obj.content.pk).text[:25]

    def content_lang(self, obj):
        return Content.objects.get(pk=obj.content.pk).lang

    content_title.short_description = 'Заголовок'
    content_text.short_description = 'Текст'
    content_lang.short_description = 'Язык'
"""


@admin.register(Work.content.through)
class ContentsOfWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text'[:40])
    search_fields = ('title', 'text')
    list_filter = ('title', 'text')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    fields = ('author', 'slug', 'pub_date')
    readonly_fields = ('pub_date',)
    save_on_top = True
    inlines = (ContentInline,)
    list_display = ('slug', 'eng_title', 'pub_date')
    search_fields = (
        'content__title',
        'content__text',
    )
    list_filter = ('author',)

    def eng_title(self, obj):

        return Content.objects.get(
            lang='eng', texts_of_project__id=obj.pk
        ).title[:25]
