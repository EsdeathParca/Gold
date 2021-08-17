import os
import qrcode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton

IMPUT_TEXT = 0


def start(update, context):
    update.message.reply_text('Hola, usa el comando: /qr  para generar un codigo qr.')

    button1 = InlineKeyboardButton(
        text= 'sobre el autor',
        url= 'https://www.facebook.com/marce.licero/')

    button2 = InlineKeyboardButton(
        text='Facebook',
        url='https://www.facebook.com')


    button3 = InlineKeyboardButton(
        text= 'Instragram',
        url= 'https://www.instagram.com')


    button4 = InlineKeyboardButton(
        text= 'Macizorras',
        url= 'https://www.macizorras.com')


    button5 = InlineKeyboardButton(
        text= 'XHAMSTER',
        url= 'https://www.xhamster.com')


    button6 = InlineKeyboardButton(
        text= 'Petardas',
        url= 'https://www.petardas.com')


    button7 = InlineKeyboardButton(
        text= 'Xvideos',
        url= 'https://www.xvideos.com')



    button8 = InlineKeyboardButton(
        text= 'Telegram',
        url= 'https://www.telegram.org')


    update.message.reply_text(
        text= 'Haz clik en un boton',
        reply_markup= InlineKeyboardMarkup([
            [button1,button2,button3,button4],
            [button5,button6,button7,button8],
        ])
    )

def qr_command_handler(update, context):
    update.message.reply_text('enviame el texto para generar un codigo QR.')

    return IMPUT_TEXT


def generate_qr(text):

    filename = text + ".jpg"

    img = qrcode.make(text)
    img.save(filename)

    return filename

def send_qr(filename, chat):

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    chat.send_photo(
        photo=open(filename, "rb")
    )

    os.unlink(filename)


def imput_text(update, context):

    text = update.message.text

    filename = generate_qr(text)

    chat = update.message.chat

    send_qr(filename, chat)


    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token='1837427715:AAE-flJuWg3hUrbeRBiEw1XnKqzkp5UNyfU', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler)
        ],

        states={
            IMPUT_TEXT: [MessageHandler(Filters.text, imput_text)]
        },

        fallbacks=[],

    ))

    updater.start_polling()
    updater.idle()