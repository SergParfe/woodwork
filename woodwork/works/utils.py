from datetime import datetime

from django.urls import resolve, reverse

from works.constants import EMAIL_TO_ME, LANGUAGE, SHORT_CARD_TEXT_LENGTH


def language_tool(language, request):
    '''
    Формирует контекст языковых значений для страницы.
    '''
    switch_to_language = (
        LANGUAGE[1] if language == LANGUAGE[0] else LANGUAGE[0]
    )
    _, _, kwargs = resolve(request.path)

    if kwargs and kwargs['language']:
        kwargs['language'] = switch_to_language
        switch_to_url = reverse(
            request.resolver_match.view_name,
            kwargs=kwargs,
        )
    else:
        switch_to_url = f'/{switch_to_language}/'

    context = {
        'language': language,
        'switch_to_language': switch_to_language,
        'switch_to_url': switch_to_url,
        'year': datetime.now().strftime('%Y'),
        'SHORT_CARD_TEXT_LENGTH': SHORT_CARD_TEXT_LENGTH,
        'EMAIL_TO_ME': EMAIL_TO_ME,
    }
    return context
