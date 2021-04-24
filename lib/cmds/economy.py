from .. import database


def coins(bot, user, *args):
	coins = database.field("SELECT Coins FROM users WHERE UserID = ?",
		user["id"])
	bot.send_message(f"{user['name']}, you have {coins:,} coins.")