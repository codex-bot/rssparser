from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER

from commands.help import CommandHelp
from commands.get import CommandGet


class Rssparser:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Rssparser module initialized")

        self.sdk.register_commands([
            ('rssparser', 'RSS parser would send you notifications from your feeds.', CommandHelp(self.sdk)),
            ('rssparser_help', 'help', CommandHelp(self.sdk)),
            ('rssparser_get', 'get', CommandGet(self.sdk))
        ])

        self.sdk.start_server()


if __name__ == "__main__":
    rssparser = Rssparser()
