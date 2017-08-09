from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))
        await self.sdk.send_text_to_chat(
            payload["chat"],
            "RSS parser follows your feeds.\n\n" \
            "Add new feed by entering a command with link to feed.\n" \
            "<code>/rssparser_add *link*</code>\n\n" \
            "Or check updates /rssparser_get",
            'HTML'
        )
