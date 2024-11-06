from serpyco_rs import Serializer

from tgbot.entities.message import Message
from tgbot.mappers.helpers import datetime_resolver

message_serializer = Serializer(
    Message,
    custom_type_resolver=datetime_resolver,
)