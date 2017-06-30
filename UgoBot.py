""" Test of Telegram Bot.

# https://github.com/python-telegram-bot/python-telegram-bot
# Name: UgoBot
# Username: @ugoBE_bot

"""

import logging
import time
import random
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import BaseFilter

listUgo = ['ugo']
listPrombi = ['prombi']
listBatman = ['batman']
listAC = ['cervelli','lavoro','work']
listHarry = ['hp','barbara','marge']
listHardcode = ['hardcoding','hardcode','hard code','hard coding','coding hard','hardcore']


isOn = False
ChatID = {-222291585: True, 388533863: True}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    global isOn
    bot.send_message(chat_id=update.message.chat_id, text="Hello Marge!")
    isOn = True

def stop(bot, update):
    global isOn
    bot.send_message(chat_id=update.message.chat_id, text="Merci Wiedersehen!")
    isOn = False

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    
def prombiloop(bot, update):
    goahead = True
    
    while goahead:
        bot.send_message(chat_id=update.message.chat_id, text="prombi")
	time.sleep(1.5)
   
        prob = random.random()
	if prob > 0.9:
	    goahead = False

def localImage(bot, update, folder, capt):
    """Sends image from local folder"""
    list_im = os.listdir(folder)
    n_im = random.randint(0, len(list_im) - 1)
    bot.sendPhoto(update.message.chat_id, open(folder + list_im[n_im], 'rb'), capt)

def readDB(file):
    """Reads a txt file as database."""
    DB = open(file, 'r')
    lines = 0
    for line in DB:
        lines = lines + 1
    DB.seek(0)    # Per tornare ad inizio file.
    n_line = random.randint(0, lines - 1)
    pick = DB.readlines()[n_line]
    DB.close()

    return pick
    
def chatID(bot, update):
    """This handler returns the chat ID when /chatID is called."""
    bot.sendMessage(chat_id=update.message.chat_id,text='The chat ID is: ' + str(update.message.chat_id))

def geoffrey_fact(bot, update):
    pick = readDB('geoffreyfacts.txt')
    bot.sendMessage(chat_id=update.message.chat_id,text='The Geoffrey Fun Fact of the Day is: ' + str(pick))

def batman_cb(bot, update):
    """ready for batman."""
    pick = readDB('batmanDB.txt')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=pick, caption="NANANANA")

def Hardcode_cb(bot, update):
    """ready for batman."""
    pick = readDB('hardcodeDB.txt')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=pick, caption="")

def AC_cb(bot, update):
    pick = readDB('ACDB.txt')
    capt = readDB('ACDB_captions.txt')
    
    rand = random.randint(0,10)
    if rand < 6:
        localImage(bot, update, "imgAC/", capt)
    else:
        pick = readDB('ACDB.txt')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=pick, caption=capt)   

def HP_cb(bot, update):
    rand = random.randint(0,4)
    if rand == 0:
        localImage(bot, update, "imgHP/", "")
    else:
        pick = readDB('HPDB.txt')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=pick)
    
class FilterUgo(BaseFilter):

    def filter(self, message):
        return any(word in message.text.lower() for word in listUgo)
	
class FilterPrombi(BaseFilter):

    def filter(self, message):
        return any(word in message.text.lower() for word in listPrombi)

class FilterBatman(BaseFilter):
    """Looks for batman"""

    def filter(self, message):
        return any(word in message.text.lower() for word in listBatman)

class FilterHardcode(BaseFilter):
    """Looks for Hardcode"""

    def filter(self, message):
        return any(word in message.text.lower() for word in listHardcode)

class FilterAC(BaseFilter):
    """Looks for AC"""

    def filter(self, message):
        return any(word in message.text.lower() for word in listAC)
	
class FilterHarryPotter(BaseFilter):
    """Looks for HP"""

    def filter(self, message):
        return any(word in message.text.lower() for word in listHarry)
	
class FilterOnOff(BaseFilter):
    def filter(self, message):
        return isOn

class FilterSensitiveMaterial(BaseFilter):
    def filter(self, message):
        if message.chat_id in ChatID:
	    return ChatID[message.chat_id]
	else:
	    return False

def main():

    updater = Updater(token='382328302:AAGB0Ad5dikuG38dgQzr1U8rdLDZgV3t2Lk')
    dispatcher = updater.dispatcher
    
    filter_Ugo = FilterUgo()
    filter_Prombi = FilterPrombi()
    filter_Batman = FilterBatman()
    filter_Hardcode = FilterHardcode()
    filter_AC = FilterAC()
    filter_Harry = FilterHarryPotter()
    filter_OnOff = FilterOnOff()
    filter_Sensitive = FilterSensitiveMaterial()

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)
    
    geoffreyfacts_handler = CommandHandler('GFFD', geoffrey_fact)
    dispatcher.add_handler(geoffreyfacts_handler)
    
    echo_handler = MessageHandler(filter_Ugo & filter_OnOff, echo)
    dispatcher.add_handler(echo_handler)
    
    prombi_handler = MessageHandler(filter_Prombi & filter_OnOff, prombiloop)
    dispatcher.add_handler(prombi_handler)
    
    chatID_handler = CommandHandler('chatID', chatID)
    dispatcher.add_handler(chatID_handler)
    
    batman_handler = MessageHandler(filter_Batman & filter_OnOff, batman_cb)
    dispatcher.add_handler(batman_handler)

    hardcode_handler = MessageHandler(filter_Hardcode & filter_OnOff, Hardcode_cb)
    dispatcher.add_handler(hardcode_handler)

    AC_handler = MessageHandler(filter_AC & filter_OnOff & filter_Sensitive, AC_cb)
    dispatcher.add_handler(AC_handler)
    
    Harry_handler = MessageHandler(filter_Harry & filter_OnOff & filter_Sensitive, HP_cb)
    dispatcher.add_handler(Harry_handler)

    updater.start_polling(clean=True)

if __name__ == '__main__':
    main()
