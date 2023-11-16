#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

#from nis import match
from random import randint, random
from ssl import Options
from subprocess import call
from termios import VQUIT
from tkinter import SW, PhotoImage
from turtle import setundobuffer, update
import telebot
import ast
import os
from telebot import types
 
crossIcon = u"\u274C"
die1face = u"\u2680"
die2face = u"\u2681"
die3face = u"\u2682"
die4face = u"\u2683"
die5face = u"\u2684"
die6face = u"\u2685"
hand_right = u"\u261E"

API_TOKEN = '5267340139:AAH_f7q774zV7fAoq61zMFZ9g56yZIKHrIY'
PATH_BASE_STANZE = 'assets/stanze/manuale_base/'
PATH_BASE_TABELLE = 'assets/tabelle/'
PATH_BASE_CHAT = 'assets/chat/'
PATH_BASE_IMG = 'assets/img/'

menu_principale = {
            'Tira 1d6' : '6', 
            'Tira 1d66': '66', 
            'Visualizza Mappa': 'map', 
            'Schede Personaggi': 'pg',
            'Flow Chart': 'flow_chart',
            'Stanze': 'mnu_stanze',
            'Tabelle': 'mnu_tabelle'
}

menu_stanze = {
    'Crea Stanza Iniziale': 'sta_init',
    'Crea Stanza': 'sta',
    '<- INDIETRO': 'mnu_principale'    
}

menu_tabelle = {
    'Tipo di mostro errante': 'tab_tipo_mostro_errante',
    'Perquisire stanza vuota': 'tab_stanza_vuota',
    'Contenuto delle stanze': 'tab_contenuto_stanza',
    'Trappole': 'tab_trappole',
    'Tesori': 'tab_tesori',
    'Tesori magici': 'tab_tesori_magici',
    'Eventi speciali': 'tab_eventi_speciali',
    'Complicazioni tesori': 'tab_complicazioni_tesori_n',
    'Caratteristiche spec': 'tab_caratteristiche_spec',
    'Incantesimi rnd': 'tab_incantesimi',
    'Missioni':'tab_missioni',
    'Ricompense Epiche': 'tab_ricompense_epiche',
    'Mostri': 'mnu_mostri',
    '<- INDIETRO': 'mnu_principale'
}

menu_mostri = {
    'Mostri Infestanti': 'tab_mostri_infestanti',
    'Mostri Seguaci': 'tab_mostri_seguaci',
    'Mostri Aberranti': 'tab_mostri_aberranti',
    'Mostri Boss': 'tab_mostri_boss',
    '<- INDIETRO': 'mnu_principale'
}

url_mappa = "<a href='https://docs.google.com/drawings/d/1JLcu-ZRp87toe99g6Op6wFnjb4GnMTv2MuYPO32-eFk/edit?usp=sharing'>Clicca qui" + hand_right + "</a>"
url_schede = "<a href='https://docs.google.com/document/d/1LVE69fMPhPIS4BC7BIGFmnnGrNtKDCL5K9QbZ1kkALI/edit?usp=sharing'>Clicca qui" + hand_right + "</a>"


bot = telebot.TeleBot(API_TOKEN)

def rollTheDice(min, faces):
    return str(randint(min, faces))

def sendPhoto(chat_id, path_image):
    # sendPhoto
    photo = open(path_image, 'rb')
    bot.send_photo(chat_id, photo)

def six(cid, message):
    #bot.send_message(cid,"You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
    bot.send_message(cid, text="Hai tirato 1d6 ed hai ottenuto\n<b>"+rollTheDice(1,6)+'</b>', parse_mode='HTML')

def double_six(cid, message):
    first_roll = str(rollTheDice(1,6))
    second_roll = str(rollTheDice(1,6))
    bot.send_message(cid, text="Hai tirato 1d66 ed hai ottenuto\n<b>"+ first_roll + second_roll+'</b>', parse_mode='HTML')

def print_file(file_path):
    file_content = 'NULL'
    #print(file_path)
    f = open(file_path,'r')
    try:
        file_content = f.read()
    except:
        print('ERR - qualcosa è andato storto - ' + file_path)
    finally:
        f.close()
        return file_content

def create_dir(cid):
    path_chat_dir = PATH_BASE_CHAT + cid
    access_rights = 0o755
    try:
        os.mkdir(path_chat_dir, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path_chat_dir)
    else:
        print ("Successfully created the directory %s" % path_chat_dir)

def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

# 
# HANDLERS
#

def map_handler(cid):
    bot.send_message(cid,"<b>Mappa: </b> " + url_mappa, parse_mode='HTML')

def pg_sheet_handler(cid):
    bot.send_message(cid,"<b>Schede dei PG:</b> "+url_schede, parse_mode='HTML')

def stanze_handler(cid, initial):
    first_roll = str(rollTheDice(1,6))
    second_roll = str(rollTheDice(1,6))

    if(initial==False):
        stanza = first_roll + second_roll
        path_photo = PATH_BASE_STANZE + 'altre/' + stanza + '.jpg'
    else: 
        stanza = first_roll
        path_photo = PATH_BASE_STANZE + 'iniziali/' + stanza + '.jpg'
    
    sendPhoto(cid, path_photo)

def show_image(cid, nome_immagine):
    path_img = PATH_BASE_IMG + nome_immagine
    sendPhoto(cid,path_img)

def tabelle_handler(cid, nome_tabella, min_voci_in_tabella, max_voci_in_tabella):
    try:
        path_voce_tabella = PATH_BASE_TABELLE + nome_tabella + '/' + str(rollTheDice(min_voci_in_tabella, max_voci_in_tabella)) + '.txt'
        #print(path_voce_tabella)
        bot.send_message(cid, print_file(path_voce_tabella), parse_mode='HTML')
    except:
        #print('ERROR')
        print('ERR - tabelle_handler - cid: ' + str(cid) + '\n\t tabella: ' + nome_tabella + '\n\t voci in tabella: ' + max_voci_in_tabella)

def menu_handler(cid, menu, header):
    bot.send_message(chat_id=cid,
                    text='Menu: ' + header,
                    reply_markup=makeKeyboard(menu),
                    parse_mode='HTML')

""" def schede_handler(cid):
    try:
        chat_type = bot.get_chat(cid).type
        admin_ids = get_admin_ids(bot, cid)
        if update.effective_user.id in admin_ids :
            print('EUREKA')
        else:
            print('booo')

        #print('id: {} chat type: {} chat member: {} - user {}' . format(cid, chat_type, chat_member))
    except NameError:
        print('ERR - schede_handler' + str(NameError)) """
    

#
# BOT MENU AND KEYBOARD
#

def makeKeyboard(menu):
    markup = types.InlineKeyboardMarkup()

    for key, value in menu.items():
        #bot.get_chat_administrators(update.message.chat.id)
        markup.add(types.InlineKeyboardButton(key, callback_data="['value', '" + value + "', '" + key + "']")) #, types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))

    return markup

@bot.message_handler(commands=['menu'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Ecco cosa puoi fare al momento",
                     reply_markup=makeKeyboard(menu_principale),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    #print(f"call.data : {call.data} , type : {type(call.data)}")
    #print(f"call : {call.message.chat.id}")
    #print(f"call : {call.message}")

    cid = call.message.chat.id

    #user = call.message.sender
    #print('You talk with user {} and his user ID: {} '.format(user.username, user.id))

    if (call.data.startswith("['value'")):
        #print(f"call.data : {call.data} , type : {type(call.data)}")
        #print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        #print("key: {}\nvalue:{}" . format(keyFromCallBack, valueFromCallBack))
        #bot.answer_callback_query(callback_query_id=call.id,
        #                      show_alert=True,
        #                      text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

        if (valueFromCallBack=='6'):
            print("Richiesta: " + "1d6")
            six(cid, call.message)

        if (valueFromCallBack=='66'):
            print("Richiesta: " + "1d66")
            double_six(cid, call.message)
        
        if (valueFromCallBack=='map'):
            print("Richiesta: " + "mappa")
            map_handler(cid)

        if (valueFromCallBack=='pg'):
            print("Richiesta: " + "PG")
            pg_sheet_handler(cid)
            
        if(valueFromCallBack=='mnu_principale'):
            print("Richiesta: " + "Menu principale")
            menu_handler(cid, menu_principale, 'MENU PRINCIPALE')
            
        if(valueFromCallBack=='mnu_stanze'):
            print("Richiesta: " + "Stanze")
            menu_handler(cid, menu_stanze, 'STANZE')

        if(valueFromCallBack=='mnu_tabelle'):
            print("Richiesta: " + "Tabelle")
            menu_handler(cid, menu_tabelle, 'TABELLE')

        if(valueFromCallBack=='mnu_mostri'):
            print("Richiesta: " + "Mostri")
            menu_handler(cid, menu_mostri, 'MOSTRI')
        
        if(valueFromCallBack=='flow_chart'):
            print("Richiesta: " + "FlowChart")
            show_image(cid,'4ad_flowchart.jpg')

        if(valueFromCallBack=='sta'):
            print("Richiesta: " + "Genera Stanze")
            stanze_handler(cid, False)
        
        if(valueFromCallBack=='sta_init'):
            print("Richiesta: " + "Genera stanza iniziale")
            stanze_handler(cid, True)
        
        if(valueFromCallBack=='tab_tipo_mostro_errante'):
            print("Richiesta: " + "Mostro errante")
            tabelle_handler(cid, 'tipo_mostro_errante', 1, 6)
        
        if(valueFromCallBack=='tab_stanza_vuota'):
            print("Richiesta: " + "Stanza Vuota")
            tabelle_handler(cid, 'perquisire_una_stanza_vuota', 1, 6)
            
        if(valueFromCallBack=='tab_contenuto_stanza'):
            print("Richiesta: " + "Contenuto stanza")
            tabelle_handler(cid, 'contenuto_stanza', 2, 12)
            
        if(valueFromCallBack=='tab_tesori'):
            print("Richiesta: " + "Tesori")
            tabelle_handler(cid, 'tesori', 1, 6)
        
        if(valueFromCallBack=='tab_tesori_magici'):
            print("Richiesta: " + "Tesori magici")
            tabelle_handler(cid,'tesori_magici', 1, 6)
        
        if(valueFromCallBack=='tab_trappole'):
            print("Richiesta: " + "Trappole")
            tabelle_handler(cid, 'trappole', 1, 6)
        
        if(valueFromCallBack=='tab_eventi_speciali'):
            print("Richiesta: " + "Eventi speciali")
            tabelle_handler(cid, 'eventi_speciali', 1, 6)

        if(valueFromCallBack=='tab_complicazioni_tesori_n'):
            print("Richiesta: " + "Complicazioni tesori")
            tabelle_handler(cid, 'complicazioni_tesori_nascosti', 1, 6)
            
        if(valueFromCallBack=='tab_caratteristiche_spec'):
            print("Richiesta: " + "Caratteristiche speciali")
            tabelle_handler(cid, 'caratteristiche_speciali', 1, 6)
        
        if(valueFromCallBack=='tab_incantesimi'):
            print("Richiesta: " + "Incantesimi")
            tabelle_handler(cid, 'incantesimi', 1, 6)

        if(valueFromCallBack=='tab_mostri_infestanti'):
            print("Richiesta: " + "Mostri infestanti")
            tabelle_handler(cid, 'mostri_infestanti', 1, 6)

        if(valueFromCallBack=='tab_mostri_seguaci'):
            print("Richiesta: " + "Mostri seguaci")
            tabelle_handler(cid, 'mostri_seguaci', 1, 6)

        if(valueFromCallBack=='tab_mostri_aberranti'):
            print("Richiesta: " + "Mostri aberranti")
            tabelle_handler(cid, 'mostri_aberranti', 1, 6)

        if(valueFromCallBack=='tab_mostri_boss'):
            print("Richiesta: " + "Mostri Boss")
            tabelle_handler(cid, 'mostri_boss', 1, 6)

        if(valueFromCallBack=='tab_missioni'):
            print("Richiesta: " + "Missioni")
            tabelle_handler(cid, 'missioni', 1, 6)

        if(valueFromCallBack=='tab_ricompense_epiche'):
            print("Richiesta: " + "Ricompense Epiche")
            tabelle_handler(cid, 'ricompense_epiche', 1, 6)
            
        #if(valueFromCallBack=='set_schede'):
            #chat_type = call.message.chat.type
        #    schede_handler(cid)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(menu_principale),
                              parse_mode='HTML')

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Ciao, sono il bot creato da Giovanni D'Addabbo per 4 Against Darkness. 
Spero ti sia utile
\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
#@bot.message_handler(func=lambda message: True)
#def echo_message(message):
#    bot.reply_to(message, message.text)

@bot.message_handler(commands=['schede', 'pg'])
def echo_message(message):
    pg_sheet_handler(message.chat.id)

@bot.message_handler(commands=['map','mappa'])
def echo_message(message):
    map_handler(message.chat.id)

@bot.message_handler(commands=['sta','stanza'])
def echo_message(message):
    stanze_handler(message.chat.id, False)

@bot.message_handler(commands=['sta_init','stanza_iniziale'])
def echo_message(message):
    stanze_handler(message.chat.id, True)

@bot.message_handler(commands=['tipo_mostro_errante'])
def echo_message(message):
    tabelle_handler(message.chat.id, 'tipo_mostro_errante', 1, 6)

@bot.message_handler(commands=['perquisire_una_stanza_vuota'])
def echo_message(message):
    tabelle_handler(message.chat.id, 'perquisire_una_stanza_vuota', 1, 6)
    
@bot.message_handler(commands=['contenuto_stanza'])
def echo_messge(message):
    tabelle_handler(message.chat.id, 'contenuto_stanza', 2, 12)

@bot.message_handler(commands=['trappole'])
def echo_messge(message):
    tabelle_handler(message.chat.id, 'trappole', 1, 6)

#@bot.message_handler(commands=['set_schede'])
#def echo_message(message):
#    schede_handler(message.chat.id)

bot.polling()


while True: # Don't let the main Thread end.
    pass