from datetime import datetime
from src.component.config import media_repository
from urllib.parse import urlparse
from itertools import chain


class MediaUniquenessChecker:
    """
    Checks message links and photos for uniqueness
    """
    def __init__(self):
        self.media_repository = media_repository

    def check(self, message):
        """
        Returns True if at least one media entity was already posted in this chat
        """
        self.media_repository.clear_stale_entries(chat_id=message.chat_id, dt=datetime.now())
        media = self.__extract_media(message)

        return self.media_repository.is_exists(chat_id=message.chat_id, medias=media)

    def __extract_media(self, message):
        def prettify_link(url):
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url

            link = urlparse(url)
            host = '.'.join(link.hostname.split('.')[-2:])
            return '{}{}#{}?{}'.format(host, link.path, link.fragment, link.query)

        def extract_photos():
            return map(lambda p: p.file_id, getattr(message.message, 'photo', []))

        def extract_urls():
            encoding = 'utf-16-le'
            utf16bytes = message.text.encode(encoding)

            for e in message.entities:
                if e.type == 'url':
                    url = utf16bytes[e.offset * 2:(e.length + e.offset) * 2].decode(encoding)
                    yield prettify_link(url)
                elif e.type == 'text_link':
                    yield prettify_link(e.url)

        return chain(extract_photos(), extract_urls())
