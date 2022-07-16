from client import base, cur


async def sqlite_add_commads(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO file_v2 VALUES (%s, %s, %s, %s, %s)", tuple(data.values()))
        base.commit()


def sqlite_del_file(title):
    cur.execute("DELETE FROM file_v2 WHERE card_name = %s", (title,))
    base.commit()


def sqlite_add_category(name):
    cur.execute("INSERT INTO categories(title) VALUES (%s) ", (name,))
    base.commit()


def sqlite_del_category(name):
    cur.execute("DELETE FROM categories WHERE title=%s", (name,))
    cur.execute("DELETE FROM file_v2 WHERE ID=%s", (name,))
    base.commit()


def get_all_user_id():
    cur.execute("SELECT user_id FROM users")
    data = cur.fetchall()
    return data


def get_today_pay():
    cur.execute("SELECT SUM(money) FROM buy")
    for i in cur.fetchone():
        return i


def get_all_orders():
    cur.execute("SELECT COUNT(money) FROM buy")
    for i in cur.fetchone():
        return i


def del_today_stat():
    cur.execute("DELETE FROM buy")
    base.commit()
