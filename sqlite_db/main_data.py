from client import bot
import Keyboard as key
from client import base, cur


def GET_GIRLS_INLINE_KEY(title):
    cur.execute("SELECT card_name FROM file_v2 WHERE ID=%s", (title,))
    data_file = cur.fetchall()
    a = []
    for row in data_file:
        a.append(row)
    base.commit()
    return a


def write_last_girl(last_girl, id):
    cur.execute("UPDATE users SET last_girl=%s WHERE user_id=%s", (last_girl, id,))
    base.commit()


async def print_card(title, id):
    write_last_girl(title, id)
    cur.execute("SELECT DISTINCT preview_id, description FROM file_v2 WHERE card_name=%s",(title,)) 
    for row in cur.fetchall():
        await bot.send_photo(id, photo=row[0], caption=row[1], reply_markup=key.buybtn)


def get_keyboard():
    get_inline_key = """SELECT title FROM categories"""
    cur.execute(get_inline_key)
    return cur.fetchall()
