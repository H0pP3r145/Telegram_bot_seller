from aiogram import Dispatcher, types
from sqlite_db import UserDB as user
import Keyboard as key
from client import bot, ADMIN_ID
from sqlite_db import main_data as data
from sqlite_db import moneyDB as money
from handlers.FAQ_h import keyboard


def Check_Call(call):
    cat = data.get_keyboard()
    for row in cat:
        if row[0] == call:
            return True


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"*{message.from_user.first_name}*, приветствуем Вас в нашем боте",
        parse_mode="MarkdownV2",
    )
    if message.get_args() != "":
        user.Check_id(message.from_user.id, message.get_args())
    else:
        user.Check_id(message.from_user.id)
    await bot.send_message(
            message.from_user.id,
            f'{message.from_user.first_name}, посколькую Вы впервые зашли в магазин <a href="https://t.me/otborniy_sok_store_bot">OS Store</a>, пожауйста, ознакомьтесь с разделом "FAQ" для понимания функционала бота!',
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    await bot.send_message(
        message.from_user.id, "Что будем делать?", reply_markup=key.Inline_key
    )


async def MainMenu(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Вы находитесь в главном меню",
        reply_markup=key.Inline_key,
    )


async def admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(
            message.from_user.id,
            "Вы в _*меню администратора*_\nЧто будем делать?",
            parse_mode="MarkdownV2",
            reply_markup=key.admin,
        )


async def inline(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "_*Выберете категорию*_",
        parse_mode="MarkdownV2",
        reply_markup=key.categories,
    )


async def category(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(
        text="_*Выберете категорию*_",
        parse_mode="MarkdownV2",
        reply_markup=key.categories,
    )


async def inline_menu_back(callback_query: types.CallbackQuery):
    user_category = user.get_last_category(callback_query.from_user.id)
    Girl = key.get_girls_key(user_category)
    await callback_query.message.delete()
    await bot.send_message(
        callback_query.from_user.id,
        f"<b>Категория</b>: <i>{user_category}</i>",
        parse_mode="HTML",
        reply_markup=Girl,
    )


async def some_callback_handler(callback_query: types.CallbackQuery):
    if Check_Call(callback_query.data) == True:
        Girl = key.get_girls_key(callback_query.data)
        user.write_last_category(callback_query.from_user.id, callback_query.data)
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.edit_text(
            text=f"<b>Категория</b>: <i>{callback_query.data}</i>",
            parse_mode="HTML",
            reply_markup=Girl,
        )
    else:
        await callback_query.message.delete()
        await data.print_card(callback_query.data, callback_query.from_user.id)


async def refer_info(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "<a href='https://telegra.ph/Kak-zarabotat-na-referalnoj-sisteme-04-23'>Как заработать на реферальной системе 🤔</a>",
        parse_mode="HTML",
    )


async def profile(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "📱 <b>Ваш профиль:</b>\n"
        + "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        + f"🔑 Мой ID: <code>{message.from_user.id}</code>\n"
        + f"👤 Логин @{message.from_user.username}\n"
        + "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        + f"💳 Баланс: <code>{money.get_balans(message.from_user.id)}</code> руб\n"
        + f"💵 Всего пополнено: <code>{money.get_all_money(message.from_user.id)}</code> руб\n"
        + f"🎁 Куплено товаров: <code>{money.get_purchased(message.from_user.id)}</code> шт\n"
        + "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        + f"💎Ваша реферальная ссылка: https://t.me/otborniy_sok_store_bot?start={message.from_user.id}\n"
        + f"🔗Активных рефералов: <code>{money.get_referal(message.from_user.id)}</code> чел\n"
        + f"💰Всего заработано с рефералов: <code>{money.get_money_via_refer(message.from_user.id)}</code> руб",
        disable_web_page_preview=True,
        parse_mode="HTML",
        reply_markup=key.profile,
    )


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(admin, commands=["admin"])
    dp.register_message_handler(inline, text="🛒 Товар")
    dp.register_message_handler(MainMenu, text="Назад в главное меню")
    dp.register_message_handler(profile, text="📱 Профиль")
    dp.register_message_handler(refer_info, text="💰 Хочу заработать 💰")
    dp.register_callback_query_handler(category, text="category")
    dp.register_callback_query_handler(inline_menu_back, text="Back")
    dp.register_callback_query_handler(
        some_callback_handler, lambda callback_query: True
    )
