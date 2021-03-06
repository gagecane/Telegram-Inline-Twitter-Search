"""Python-based Telegram bot

python-telegram-bot documentation: https://python-telegram-bot.readthedocs.io/en/stable/

"""

import logging

from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def load_bot_token_from_file(filename):
    with open(filename, 'r') as tokenfile:
        return tokenfile.readlines()[0].strip()


def load_keys_from_json(self, key_file=None):
    """Load consumer keys from a json file

    Keyword Arguments:
        keyFile {string} -- Optional keyFile name. Will use self.keyFile
                            if not populated (default: {None})
    """
    key_file_to_read = key_file
    if (key_file is None):
        key_file_to_read = self.keyFile
    try:
        with open(key_file_to_read, 'r') as open_key_file:
            self.keys = json.load(open_key_file)
    except TypeError:
        print("Error: expected a string for filename")
    except FileNotFoundError:
        print(f"Error: File {key_file_to_read} does not exist")


def connect_to_twitter():
    """Connect to twitter
    """
    return


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(load_bot_token_from_file("token.txt"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
