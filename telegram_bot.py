import telegram

class TelegramBot:

    def __init__(self, token):
        self.token = token
        self.bot = telegram.Bot(token = self.token)
    
    def sendMessage(self, chat_id, message):
        self.bot.sendMessage(chat_id = chat_id, text=message)

    def getChatId(self):
        return self.bot.getUpdates()[-1].message.chat.id


if __name__ == "__main__":
    token = "********" # your token
    bot = TelegramBot(token)
    # receiver_id = 00000000 # your id

    chat_id = bot.getChatId()
    print(chat_id)

    bot.sendMessage(chat_id, "Hello")