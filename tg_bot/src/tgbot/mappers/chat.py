from serpyco_rs import Serializer

from tgbot.entities.chat import Chat
from tgbot.mappers.helpers import datetime_resolver

chat_serializer = Serializer(
    Chat,
    custom_type_resolver=datetime_resolver,
)
