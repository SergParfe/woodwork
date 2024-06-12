from datetime import datetime

from django.urls import reverse

from works.constants import LANGUAGE


def language_tool(language, request):
    '''
    Формирует словарь языковых значений для страницы.
    '''
    language = LANGUAGE[0] if language not in LANGUAGE else language
    switch_to_language = (
        LANGUAGE[1] if language == LANGUAGE[0] else LANGUAGE[0]
    )
    path = request.path
    switch_to_url = (
        f'{path}{switch_to_language}/'
        if path == '/'
        else reverse(
            request.resolver_match.view_name,
            kwargs={'language': switch_to_language},
        )
    )
    context = {
        'language': language,
        'year': datetime.now().strftime('%Y'),
        'switch_to_language': switch_to_language,
        'switch_to_url': switch_to_url,
    }
    return language, context
