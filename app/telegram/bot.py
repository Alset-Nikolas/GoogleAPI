import telebot


class Bot:
    def __init__(self, token, group_id) -> None:
        self.bot = telebot.TeleBot(token)
        self.group_id = group_id

    def send_message(self, msg):
        self.bot.send_message(self.group_id, msg)
