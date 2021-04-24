from random import choice, randint
from time import time

from .. import database

heist = None
heist_lock = time()


def coinflip(bot, user, side=None, *args):
    if side is None:
        bot.send_message("You need to guess which side the coin will land!")

    elif (side := side.lower()) not in (opt := ("h", "t", "heads", "tails")):
        bot.send_message("Enter one of the following as the side: " + ", ".join(opt))

    else:
        result = choice(("heads", "tails"))

        if side[0] == result[0]:
            database.execute("UPDATE users SET Coins = Coins + 50 WHERE UserID = ?",
                       user["id"])
            bot.send_message(f"It landed on {result} and you won 50 coins PagMan ")

        else:
            bot.send_message(f"Too bad - it landed on {result}. You didn't win anything Sadge ")


class Heist(object):
    def __init__(self):
        self.users = []
        self.running = False
        self.start_time = time() + 60
        self.end_time = 0
        self.messages = {
            "success": [
                "{} fought off the guards, and got their haul EZ ",
                "{} sneaked out of the back entrance with their share EZ ",
                "{} got in and out seemlessly with their money EZ ",
            ],
            "fail": [
                "{} got caught by the guards widepeepoSad ",
                "{} was injured by a gunshot widepeepoSad ",
                "{} got lost! widepeepoSad ",
            ]
        }

    def add_user(self, bot, user, bet):
        if self.running:
            bot.send_message("Heist already in progress. Wait until the next one Pepega ")

        elif user in self.users:
            bot.send_message("You're already good to go.")

        elif bet > (coins := database.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])):
            bot.send_message(f"You don't have that much to bet - you only have {coins:,} coins.")

        else:
            database.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
                       bet, user["id"])
            self.users.append((user, bet))
            bot.send_message("You're all suited and ready to go EZ Wait for a minute or two now and use command again to check reults ")

    def start(self, bot):
        bot.send_message("The heist has started! Wait")
        self.running = True
        self.end_time = time() + randint(30, 50)

    def end(self, bot):
        succeeded = []

        for user, bet in self.users:
            if randint(0, 1):
                database.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                           bet * 1.5, user["id"])
                succeeded.append((user, bet * 1.5))
                bot.send_message(choice(self.messages["success"]).format(user["name"]))

            else:
                bot.send_message(choice(self.messages["fail"]).format(user["name"]))

        if len(succeeded) > 0:
            bot.send_message("The heist is over Pog "
                             + ", ".join([f"{user['name']} got {coins:,} coins" for user, coins in succeeded]))

        else:
            bot.send_message("Heist failed.... No one got out Sadge ")


def start_heist(bot, user, bet=None, *args):
    global heist

    if bet is None:
        bot.send_message("You need to specify an amount to bet Pepega ")

    else:
        try:
            bet = int(bet)

        except ValueError:
            bot.send_message("That's not a valid bet.")

        else:
            if bet < 1:
                bot.send_message("You need to bet at least 1 coin.")

            else:
                if heist is None:
                    heist = Heist()

                heist.add_user(bot, user, bet)


def run_heist(bot):
    heist.start(bot)


def end_heist(bot):
    global heist

    heist.end(bot)
    heist = None
