from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))
        await self.sdk.send_text_to_chat(
            payload["chat"],
            "RSS parser follows your feeds.\n\n" \
            "/rssparser_list — show list of your feeds\n" \
            "/rssparser_add — add new feed\n" \
            "/rssparser_get — check updates\n" \
            "/rssparser_remove — remove subscription\n",
            'HTML'
        )
