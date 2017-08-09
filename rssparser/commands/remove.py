from config import CHATS_COLLECTION_NAME
from .base import CommandBase


class CommandRemove(CommandBase):

    async def __call__(self, payload):

        feed_link = payload['params']

        if not feed_link:
            self.sdk.log("No feed link was passed")
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "Remove subscription by entering a command with link.\n" \
                "<code>/rssparser_remove *link*</code>",
                "HTML"
            )

        chat_token = payload['chat']
        registered_chat = self.sdk.db.find_one(CHATS_COLLECTION_NAME, {'chat': chat_token})

        if not registered_chat:
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "It looks like you have no connected feeds.\n" \
                "Add first one by /rssparser_add."
            )

        links = registered_chat['links']

        # save link
        link_is_not_in_list = True
        for link in links:
            if link['link'] == feed_link:
                link_is_not_in_list = False
                break

        if link_is_not_in_list:
            self.sdk.log("No feed to remove")
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "No feed with this link was found."
            )
        else:
            new_links_list = []
            for link in links:
                if link['link'] != feed_link:
                    new_links_list.append(link)
            self.sdk.log("New list of feeds was created")

        self.sdk.db.update(CHATS_COLLECTION_NAME, {'chat': chat_token}, {"$set": {'links': new_links_list}})

        await self.sdk.send_text_to_chat(
            payload["chat"],
            "You have removed this feed."
        )
