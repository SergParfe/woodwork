from datetime import datetime

from django.urls import NoReverseMatch, reverse

from works.constants import LANGUAGE


def language_tool(language, request):
    '''
    Формирует контекст языковых значений для страницы.
    '''
    switch_to_language = (
        LANGUAGE[1] if language == LANGUAGE[0] else LANGUAGE[0]
    )
    path = request.path
    try:
        switch_to_url = (
            f'{path}{switch_to_language}/'
            if path == '/'
            else reverse(
                request.resolver_match.view_name,
                kwargs={'language': switch_to_language},
            )
        )
    except NoReverseMatch:
        switch_to_url = f'/{switch_to_language}/'
    context = {
        'language': language,
        'switch_to_language': switch_to_language,
        'switch_to_url': switch_to_url,
        'year': datetime.now().strftime('%Y'),
    }
    return context
