from sqlite_db import UserDB as user
from client import base, cur

# get_commands-------


def get_balans(id):
    cur.execute("SELECT money FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


def get_all_money(id):
    cur.execute("SELECT all_money FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


def get_purchased(id):
    cur.execute("SELECT purchased FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


# -------------------------


def get_referal(id):
    cur.execute("SELECT refer FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


def add_referal(id_user, id_dad):
    if user.bool_check_id(id_user) == False:
        cur.execute(
            "UPDATE users SET refer=%s WHERE user_id=%s",
            (get_referal(id_dad) + 1, id_dad),
        )
        base.commit()


def is_refer(id):
    cur.execute("SELECT refer_id FROM users WHERE user_id=%s", (id,))
    return True if cur.fetchone()[0] != 0 else False


def get_my_referal(id):
    cur.execute("SELECT refer_id FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


def add_refer_money(id, money):
    money_dad = cur.execute(
        "SELECT refer_money FROM users WHERE user_id=%s", (id,)
    ).fetchone()[0]
    cur.execute(
        "UPDATE users SET refer_money=%s WHERE user_id=%s", (money + money_dad, id)
    )
    base.commit()


def add_money_to_referal(id, money):
    if is_refer(id):
        refer = get_my_referal(id)
        cur.execute(
            "UPDATE users SET money=%s WHERE user_id=%s",
            ((money) + get_balans(refer), refer),
        )
        base.commit()
        add_refer_money(refer, money)


def get_money_via_refer(id):
    cur.execute("SELECT refer_money FROM users WHERE user_id=%s", (id,))
    for i in cur.fetchone():
        return i


# -----------------------------


def add_purchased(id):
    cur.execute(
        "UPDATE users SET purchased=%s WHERE user_id=%s", (get_purchased(id) + 1, id)
    )
    base.commit()


def add_allmoney(id, money):
    cur.execute(
        "UPDATE users SET all_money=%s WHERE user_id=%s", (get_all_money(id) + money, id)
    )
    base.commit()


def add_money(id, money):
    cur.execute(
        "UPDATE users SET money=%s WHERE user_id=%s", (get_balans(id) + money, id)
    )
    base.commit()
    add_money_to_referal(id, money)
    add_allmoney(id, money)


def minus_money(id, money):
    cur.execute(
        "UPDATE users SET money=%s WHERE user_id=%s", (get_balans(id) - money, id)
    )
    base.commit()


# ------------------------------------------


def get_file(id):
    cur.execute(
        "SELECT file_id FROM file_v2 WHERE card_name=%s", (user.get_last_girl(id),)
    )
    for i in cur.fetchone():
        return i


# ----------------------------------------------------


def add_payments_par(user_id=None, money=None, bill_id=None):
    cur.execute(
        "INSERT INTO buy (user_id, money, bill_id) VALUES (%s, %s, %s)",
        (
            user_id,
            money,
            bill_id,
        ),
    )
    base.commit()


def get_payments_par(bill_id):
    result = cur.execute("SELECT * FROM buy WHERE bill_id =%s", (bill_id)).fetchmany(1)
    return False if not bool(len(result)) else result


def get_added_money(user_id):
    cur.execute("SELECT money FROM buy WHERE user_id=%s", (user_id,))
    for i in cur.fetchone():
        return i


def delete_bill_id(bill_id):
    cur.execute("DELETE FROM buy WHERE bill_id=%s", (bill_id,))
    base.commit()
