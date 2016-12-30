from datetime import datetime
from src.config import media_repository
from urllib.parse import urlparse
from src.domain.message import Message
from typing import List


class MediaUniquenessChecker:
    """
    Checks message links and photos for uniqueness
    """
    def __init__(self):
        self.media_repository = media_repository

    def check(self, message: Message):
        """
        Returns True if at least one media entity was already in this chat
        """
        self.media_repository.clear_stale_entries(chat_id=message.chat_id, dt=datetime.now())
        media = self.__extract_media(message)

        return self.media_repository.is_exists(chat_id=message.chat_id, media_list=media)

    def __extract_media(self, message: Message) -> List[str]:
        media = []

        for entity in filter(lambda e: e.type == 'url', message.entities):
            link = self.__prettify(message.text[entity.offset:entity.length + entity.offset])
            media.append(link)

        media += list(map(lambda p: p.file_id, getattr(message.message, 'photo', [])))

        return media

    def __prettify(self, url: str) -> str:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        link = urlparse(url)
        host = '.'.join(link.hostname.split('.')[-2:])
        return '{}{}#{}?{}'.format(host, link.path, link.fragment, link.query)
