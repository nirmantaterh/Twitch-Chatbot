from datetime import timedelta
from sys import exit
from time import time
from random import randint

from .. import database

BOOT_TIME = time()
OWNER = "nic0nee"


def help(bot, prefix, cmds):
	bot.send_message(f"Registered commands: "
		+ ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))


def about(bot, user ,*args):
	bot.send_message("Chat bot made for Twitch specfically by Nirman Taterh PagMan ")


def hello(bot, user, *args):
	bot.send_message(f"Hey {user['name']}!")


def uptime(bot, user, *args):
	bot.send_message(f"The bot has been online for {timedelta(seconds=time()-BOOT_TIME)}.")


def userinfo(bot, user, *args):
	bot.send_message(f"Name: {user['name']}. ID: {user['id']}.")

def heightcheck(bot,user,*args):
	bot.send_message(f"{user['name']} woke up feeling {random.randint(150,200)} cm")

def shutdown(bot, user, *args):
	if user["name"].lower() == OWNER:
		bot.send_message("Shutting down.")
		database.commit()
		database.close()
		bot.disconnect()
		exit(0)

	else:
		bot.send_message("You can't do that.(only for mods)")
