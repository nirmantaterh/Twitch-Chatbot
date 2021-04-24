from irc.bot import SingleServerIRCBot
from requests import get

from lib import database, cmds, msgreact, automoderation

NAME = "NAME OF YOUR BOT's ACCOUNT"
OWNER = "NAME OF STREAMERS ACCOUNT"	


class Bot(SingleServerIRCBot):
	def __init__(self):
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = "GET UR CLIENT ID BY REGISTERING IN TWITCH"      """ cannot share my id but it will be a long alphanumeric sequence """
		self.TOKEN = "GET OAUTH ID FROM TWITCH GENERATOR"
		self.CHANNEL = f"#{OWNER}"

		url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
		headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
		resp = get(url, headers=headers).json()
		self.channel_id = resp["users"][0]["_id"]

		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

	def on_welcome(self, cxn, event):
		for req in ("membership", "tags", "commands"):
			cxn.cap("REQ", f":twitch.tv/{req}")

		cxn.join(self.CHANNEL)
		database.build()
		self.send_message("Now online.")

	@database.with_commit
	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		msgreact.add_user(bot, user)

		if user["name"] != NAME and automoderation.clear(bot, user, message):
			msgreact.process(bot, user, message)
			cmds.process(bot, user, message)

	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
	bot = Bot()
	bot.start()
