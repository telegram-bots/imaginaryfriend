from src.handler.messages.base import Base
from src.handler.messages.message_processor import MessageProcessor
from src.handler.messages.media_checker import MediaChecker
from src.handler.messages.sticker_spammer import StickerSpammer

message_handlers = [clazz() for clazz in Base.__subclasses__()]
