import telebot
from telebot import types
import pyautogui
import random
import string
from tkinter import Tk, Label, PhotoImage, Entry, Button

bot = telebot.TeleBot('YOUR_BOT_TOKEN') # enter your bot token
password = ""

def screenlock(chat_id):
    root = Tk()
    root.title("Screen Locked")

    photo = PhotoImage(file="path/to/your/image.png") # enter path to your imege for screenlock
    label = Label(root, image=photo)
    label.pack()

    entry_label = Label(root, text="Enter Password:")
    entry_label.pack()

    entry = Entry(root, show="*")
    entry.pack()

    unlock_button = Button(root, text="Unlock", command=lambda: unlock_screen(entry.get(), chat_id, root))
    unlock_button.pack()

    root.mainloop()

def unlock_screen(user_input, chat_id, root):
    global password
    if user_input == password:
        pyautogui.press('enter')
        bot.send_message(chat_id, "Monitor was unlocked")
        root.destroy()
    else:
        bot.send_message(chat_id, "Wrong password")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "For more information input command /help")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "How to use:\n"
                                      "/lock - monitor locking\n"
                                      "/set_password - password setting\n"
                                      "/unlock - monitor unlocking")

@bot.message_handler(commands=['lock'])
def lock(message):
    screenlock(message.chat.id)
    bot.send_message(message.chat.id, "Monitor is now locked")

def generate_password():
    password_length = 8
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))
    if not any(char.isupper() for char in password):
        password += random.choice(string.ascii_uppercase)
    if not any(char.islower() for char in password):
        password += random.choice(string.ascii_lowercase)
    if not any(char.isdigit() for char in password):
        password += random.choice(string.digits)
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

@bot.message_handler(commands=['set_password'])
def set_password(message):
    global password
    password = generate_password()
    bot.send_message(message.chat.id, f"Password has been set: {password}")

@bot.message_handler(commands=['unlock'])
def unlock(message):
    bot.send_message(message.chat.id, "Use the /lock command to lock the screen.")
    
bot.polling()