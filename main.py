from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == '__main__':

    logger.add('debuglog.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {name} : {function} : {line} | {message}',
               level='WARNING', rotation='1 day')
    logger.add('catch_log.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {name} : {function} : {line} | {message}',
               filter=lambda record: 'special' in record['extra'], rotation='1 day')
    logger.add('user_actions.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {name} : {function} | {message}',
               level='INFO', rotation='1 day')

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
