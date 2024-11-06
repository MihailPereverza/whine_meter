from serpyco_rs import Serializer

from tgbot.entities.user import User
from tgbot.mappers.helpers import datetime_resolver

user_serializer = Serializer(
    User,
    custom_type_resolver=datetime_resolver,
)
