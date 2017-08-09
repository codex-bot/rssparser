from config import CHATS_COLLECTION_NAME
from .base import CommandBase


class CommandList(CommandBase):

    async def __call__(self, payload):

        chat_token = payload['chat']
        registered_chat = self.sdk.db.find_one(CHATS_COLLECTION_NAME, {'chat': chat_token})

        if not registered_chat:
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "It looks like you have no connected feeds.\n" \
                "Add first one by /rssparser_add."
            )

        feeds = registered_chat.get('links')

        if not feeds:
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "It looks like you have no connected feeds.\n" \
                "Add first one by /rssparser_add."
            )

        message = "Your connected feeds:\n\n"

        for feed in feeds:
            message += "«{}» — {}\n".format(feed['title'], feed['link'])

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )
