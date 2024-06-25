import logging
import urllib.parse
import urllib.request
from datetime import datetime

from django.conf import settings
from django.urls import resolve, reverse

from works.constants import (
    EMAIL_TO_ME,
    LANGUAGE,
    SHORT_CARD_TEXT_LENGTH,
    SWITCH_TO_LABELS,
)


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
        'switch_to_url': switch_to_url,
        'switch_to_label': SWITCH_TO_LABELS[switch_to_language],
        'year': datetime.now().strftime('%Y'),
        'SHORT_CARD_TEXT_LENGTH': SHORT_CARD_TEXT_LENGTH,
        'EMAIL_TO_ME': EMAIL_TO_ME,
    }
    return context


def send_telegram_message(message_text):
    '''Отправка комментария в Телеграм.'''

    logger = logging.getLogger('send_to_gram')
    if settings.TELEGRAM_TOKEN and settings.TELEGRAM_TO:

        url = ''.join(
            [
                'https://api.telegram.org/bot',
                f'{settings.TELEGRAM_TOKEN}/sendMessage',
            ]
        )

        data = urllib.parse.urlencode(
            {'chat_id': settings.TELEGRAM_TO, 'text': message_text}
        )
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        try:

            response = urllib.request.urlopen(req)
            logger.info(
                f'Telegram response: {response.read().decode("utf-8")}'
            )
        except urllib.error.HTTPError as e:
            logger.error(f'Error sending message: {e.code}')
