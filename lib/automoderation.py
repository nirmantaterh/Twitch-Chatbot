from collections import defaultdict

from . import database

CURSES = ("","","") """Enter banned words here"""
warning_timers = (10, 30, 90)


def clear(bot, user, message):
	if any([curse in message for curse in CURSES]):
		warn(bot, user, reason="Cursing")
		return False

	return True


def warn(bot, user, *, reason=None):
	warnings = database.field("SELECT Warnings FROM users WHERE UserID = ?",
		user["id"])

	if warnings < len(warning_timers):
		mins = warning_timers[warnings]
		bot.send_message(f"/timeout {user['name']} {mins}m")
		bot.send_message(f"{user['name']}, you have been muted for the following reason: {reason} and will be unmuted in {mins} mins.")

		database.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?",
			user["id"])

	else:
		bot.send_message(f"/ban {user['name']} repeated offensive behaviour ")
		bot.send_message(f"{user['name']}, you have been banned from chat ")
