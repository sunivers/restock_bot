import configparser
from bs4 import BeautifulSoup
from restock import StockCheck
from telegram_bot import TelegramBot
from datetime import datetime
import time

# Loading config
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize scraping classes
# TODO Consider function to lambda

def itemStockCheck(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    stock_div = soup.find("div", attrs={"id": "addToCartFormHolder"})

    if stock_div == None:
        return False

    class_list = stock_div['class']
    
    if 'hide' in class_list:
        return False

    return True

# main script
if __name__ == "__main__":
    bot = TelegramBot(config['TELEGRAM']['TOKEN'])
    chat_ids = config.get('TELEGRAM', 'RECEIVER_ID').split(', ')
    bot.sendMessage(chat_ids[0], "Monitoring started.")

    multi_pochette_accessoires = StockCheck("멀티 포쉐트 악세수아"
        , "https://kr.louisvuitton.com/kor-kr/products/multi-pochette-accessoires-monogram-nvprod1770359v"
        , itemStockCheck, "utf-8")
    
    felicie_pochette = StockCheck("포쉐트 펠리시", "https://kr.louisvuitton.com/kor-kr/products/felicie-pochette-monogram-010578#M61276", itemStockCheck, "utf-8")

    sleep_mins = config['DEFAULT']['INTERVAL_MINS']


    def check(checkTargetArray):
        return list(map(lambda item: item.statusChanged(), checkTargetArray))


    while True:
        returns = check([multi_pochette_accessoires, felicie_pochette])

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), returns)
        for user in chat_ids:
            bot.sendMessage(user, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        alerts = list(filter(lambda item: item[0] , returns))

        for item in alerts:
            for user in chat_ids:
                bot.sendMessage(user, "{} - 재고 상태 변경 : {}".format(item[3].name, item[0]))
        
        time.sleep(int(sleep_mins) * 60)