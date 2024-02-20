from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(bot):
    await bot.set_my_commands(
        [BotCommand(*command) for command in DEFAULT_COMMANDS]
    )