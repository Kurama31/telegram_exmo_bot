import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
import requests
############################### Key ############################################
key = '......'
#https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/
############################### \Key ############################################

############################### log ############################################
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
print('Log of INFO: -> ' + str(logger))
############################### \log ############################################

############################### REST API to EXMO ############################################
def request_exchange_course(event):
    url = "https://api.exmo.com/v1.1/order_book"
    payload='pair={}_RUB&limit=0'.format(event)
    #print('event', event)

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response_json = requests.request("POST", url, headers=headers, data=payload).json()
    response_str = response_json['{}_RUB'.format(event)]['ask_top']
    #print('response_str', response_str)
    #result = response_str.split('.')[0] + ',' + response_str.split('.')[1] + ' RUB'
    result = response_str
    return result
############################### \REST API to EXMO ############################################

############################### bot ############################################
  
  
FIRST = range(1)

def start(update: Update, context: CallbackContext) -> None:
    user = update.message #.from_user
    logger.info("User %s started the conversation.", user )#.first_name

    """Sends a message with some inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("ETH (Etherium)", callback_data='{}'.format('ETH') ),
            InlineKeyboardButton("BTC", callback_data='{}'.format('BTC') ),
        ],
        [
            InlineKeyboardButton("second menu", callback_data='second menu')
            #InlineKeyboardButton("stop", callback_data='stop'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose a cryptocurrency:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query #обратный запрос

    # See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    #print('query.answer()' , query.answer())


    response_str = request_exchange_course(query.data)
    query.edit_message_text('Exchange Rates of {} 1 = {}'.format(query.data, response_str))

def second_menu(update: Update, context: CallbackContext):
    query = update.callback_query #обратный запрос
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("(second_menu) 1", callback_data=str('ONE')),
            InlineKeyboardButton("(second_menu) 2", callback_data=str('TWO')),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)


############################# Handlers ######################################### (Обработчики)
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(key)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler('button', button)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    updater.dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()