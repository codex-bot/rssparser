from config import CHATS_COLLECTION_NAME
from .base import CommandBase
from .get import CommandGet
import time
import feedparser


class CommandAdd(CommandBase):

    async def __call__(self, payload):

        feed_link = payload['params']

        if not feed_link:
            self.sdk.log("No feed link was passed")
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "Add new feed by entering a command with link to feed.\n" \
                "<code>/rssparser_add *link*</code>",
                "HTML"
            )

        # check link
        feed = feedparser.parse(feed_link)
        if not feed.get('feed'):
            self.sdk.log("Error while parsing feed {}".format(feed_link))
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "I can't parse this feed. Check link."
            )
        feed_title = feed['feed']['title']

        chat_token = payload['chat']

        registered_chat = self.sdk.db.find_one(CHATS_COLLECTION_NAME, {'chat': chat_token})

        if registered_chat:
            links = registered_chat['links']
        else:
            new_chat = {
                'chat': chat_token,
                'links': []
            }
            self.sdk.db.insert(CHATS_COLLECTION_NAME, new_chat)
            self.sdk.log("New chat registered with token {}".format(chat_token))

            # add scheduler
            payload['command'] = 'rssparser_get'
            payload['params'] = 'scheduler'
            self.sdk.scheduler.add(
                CommandGet(self.sdk).run,
                chat_id=chat_token,
                args=[payload],
                hour='*'
            )
            links = []

        # save link
        link_is_not_in_list = True
        for link in links:
            if link['link'] == feed_link:
                link_is_not_in_list = False
                break

        if link_is_not_in_list:
            links.append({'title': feed_title, 'link': feed_link, 'last_check': time.time()})
            self.sdk.log("New feed link was added to chat {}".format(chat_token))
        else:
            self.sdk.log("Passed feed link already exist in chat {}".format(chat_token))
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "This feed is already connected."
            )

        self.sdk.db.update(CHATS_COLLECTION_NAME, {'chat': chat_token}, {"$set": {'links': links}})

        await self.sdk.send_text_to_chat(
            payload["chat"],
            "From this moment we follow «{}».".format(feed_title)
        )
