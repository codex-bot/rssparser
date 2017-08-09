from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER

from commands.help import CommandHelp
from commands.list import CommandList
from commands.add import CommandAdd
from commands.get import CommandGet
from commands.remove import CommandRemove


class Rssparser:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Rssparser module initialized")

        self.sdk.register_commands([
            ('rssparser', 'RSS parser follows your feeds.', CommandHelp(self.sdk)),
            ('rssparser_list', 'Show list of your feeds.', CommandList(self.sdk)),
            ('rssparser_add', 'Add new feed.', CommandAdd(self.sdk)),
            ('rssparser_get', 'Check your feed right now.', CommandGet(self.sdk).run),
            ('rssparser_remove', 'Remove subscription.', CommandRemove(self.sdk))
        ])

        self.sdk.scheduler.restore(self.processor)

        self.sdk.start_server()

    def processor(self, params):
        return CommandGet(self.sdk).run

if __name__ == "__main__":
    rssparser = Rssparser()
