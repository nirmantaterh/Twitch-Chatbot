from collections import defaultdict
from datetime import datetime, timedelta
from random import randint
from re import search
from time import time

from . import database
from .cmds import fun

welcomed = []
messages = defaultdict(int)


def process(bot, user, message):
	update_records(bot, user)

	if user["id"] not in welcomed:
		welcome(bot, user)

	elif "bye" in message:
		say_goodatabaseye(bot, user)
		
	if (match := search(r'cheer[0-9]+', message)) is not None:
		thank_for_cheer(bot, user, match)

	if (h := fun.heist) is not None:
		if h.start_time <= time() and not h.running:
			fun.run_heist(bot)

		elif h.end_time <= time() and h.running:
			fun.end_heist(bot)


def add_user(bot, user):
	database.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)",
		user["id"], user["name"].lower())


def update_records(bot, user):
	database.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent + 1 WHERE UserID = ?",
		user["name"].lower(), user["id"])

	stamp = database.field("SELECT CoinLock FROM users WHERE UserID = ?",
		user["id"])

	if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
		coinlock = (datetime.utcnow()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")

		database.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?",
			randint(1, 5), coinlock, user["id"])


def welcome(bot, user):
	bot.send_message(f"Welcome to the stream {user['name']}!")
	welcomed.append(user["id"])


def say_goodatabaseye(bot, user):
	bot.send_message(f"See ya later {user['name']}!")
	welcomed.remove(user["id"])

def check_activity(bot, user):
	messages[user["id"]] += 1
	
"""def thank_for_cheer(bot, user, match):
	bot.send_message(f"Thanks for the {match.group[5:]:,} bits {user['name']}! That's really appreciated!")"""
