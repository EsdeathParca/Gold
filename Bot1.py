from telegram.ext import Updater, CommandHandler


def start(update, context):

    update.message.reply_text('¿Qué mejor manera de morir, que por la cenizas de tus padres y el templo de tus dioses?')



if __name__ == '__main__':

    updater = Updater(token='your token', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
