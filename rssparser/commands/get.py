from config import CHATS_COLLECTION_NAME
from .base import CommandBase
import feedparser
import time
from dateutil.parser import parse as dateparser


class CommandGet(CommandBase):

    async def run(self, payload):

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

        is_no_new_items = True

        updated_feeds = []

        for feed in feeds:
            parsed = feedparser.parse(feed['link'])
            entries = parsed.get('entries')

            last_check = feed['last_check']

            for entry in reversed(entries):
                try:
                    publishing_date = dateparser(entry.get('published') or entry.get('updated')).timestamp()
                    if publishing_date > last_check:
                        message = "{}: <a href=\"{}\">{}</a>".format(feed['title'], entry['link'], entry['title'])
                        await self.sdk.send_text_to_chat(
                            payload["chat"],
                            message,
                            "HTML"
                        )
                        is_no_new_items = False
                except:
                    self.sdk.log("{} feed's items have no published date.".format(feed['link']))
            feed['last_check'] = time.time()
            updated_feeds.append(feed)

        self.sdk.db.update(CHATS_COLLECTION_NAME, {'chat': chat_token}, {"$set": {'links': updated_feeds}})

        if payload['params'] != 'scheduler' and is_no_new_items:
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "No updates for you at this moment."
            )
