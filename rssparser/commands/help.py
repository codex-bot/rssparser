from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))
        await self.sdk.send_text_to_chat(
            payload["chat"],
            "Try using by enter command\n\n" \
            "/rssparser_get *link*"
        )
