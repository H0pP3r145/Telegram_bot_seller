from aiogram import executor
import logging
from handlers import users_h, help_h, buy, qiwi, FAQ_h
from handlers.admin_handlers import (
    admin_add_file,
    admin_del_file,
    admin_add_category,
    admin_del_category,
    admin_commad,
)
from Test_photo import test_photo_h
from client import dp, bot, URL_APP, base, cur
from sqlite_db import AdminDATA
import os

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    await bot.set_webhook(URL_APP)

async def on_shutdown(_):
    await bot.delete_webhook()
    cur.close()
    base.close()


FAQ_h.register_FAQ_information(dp)
qiwi.register_buy_handler(dp)
buy.register_pay_handler(dp)
test_photo_h.register_test_photo(dp)
admin_commad.register_admin_command_handler(dp)
admin_add_file.register_handlers_admin(dp)
admin_del_file.register_handlers_admin(dp)
admin_add_category.register_handlers_add_cat(dp)
admin_del_category.register_handlers_del_cat(dp)
users_h.register_handlers_users(dp)
help_h.register_message_help(dp)

executor.start_webhook(
    dispatcher=dp, 
    webhook_path='', 
    on_startup=on_startup, 
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)))
