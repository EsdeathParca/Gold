import os
import qrcode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton



IMPUT_TEXT = 0


def start(update, context):

    update.message.reply_text(
         text= 'Hola, ¿Qué deseas hacer?',
         reply_markup=InlineKeyboardMarkup([
              [InlineKeyboardButton(text='Generar qr', callback_data='qr')],
              [InlineKeyboardButton(text='Sobre el autor', url='www.facebook.com')],
             ])
    )


def qr_command_handler(update, context):
    update.message.reply_text('enviame el texto para generar un codigo QR.')

    return IMPUT_TEXT


def qr_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Envíame el texto para generar el codigo Qr'
    )

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
    updater = Updater(token='your token', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
        ],

        states={
            IMPUT_TEXT: [MessageHandler(Filters.text, imput_text)]
        },

        fallbacks=[],

    ))

    updater.start_polling()
    updater.idle()
