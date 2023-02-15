import os
import sqlite3
import datetime
from settings import database_name as db
import random


def get_fake_name(length=3):
    vowel = "aeiouy"  # гласные
    consonant = "bcdfghjklmnpqrstvwxz"  # согласные
    name = ""
    j = 0
    while j < length:
        name += random.choice(consonant)
        name += random.choice(vowel)
        j += 1
    return name.capitalize()


def get_random_number(mn=100, mx=999):
    return random.randrange(mn, mx)


def delete_database(**kwargs):
    if not os.path.exists(db):
        create_database()

    username = kwargs.get("username")
    idx_lst = list()
    if username:
        slct = f"SELECT id FROM person WHERE username LIKE '{username}'"
        con = sqlite3.connect(db)
        with con:
            idx_lst = [row[0] for row in con.execute(slct)]

    idx = kwargs.get("id")
    idx_lst = [idx] if idx else idx_lst
    id_str = f"({','.join(map(str, idx_lst))})"
    today = f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    upd = f"UPDATE person SET deleted = '{today}' WHERE id in {id_str}"
    con = sqlite3.connect(db)
    with con:
        con.execute(upd)
    return {"Ok": True}


def update_database(**kwargs):
    username = kwargs.get("username")
    if not username:
        return {"Ok": False}
    if not os.path.exists(db):
        create_database()
    score = kwargs.get("score", 0)
    duration = kwargs.get("duration", 0)
    today = f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    upd = f"""
        INSERT INTO person (
            username,
            score,
            duration,
            created,
            deleted
            ) 
        VALUES (
            '{username}','{score}', {duration}, '{today}','{None}'
            )
    """
    con = sqlite3.connect(db)
    with con:
        con.execute(upd)
    return {"Ok": True}


def read_database(length=10):
    ret_dct = dict()
    if not os.path.exists(db):
        create_database()
        return ret_dct
    read = f"SELECT username, score FROM person WHERE deleted = 'None' ORDER BY score DESC LIMIT {length}"
    con = sqlite3.connect(db)
    ret_dct = dict()
    with con:
        for num, row in enumerate(con.execute(read), 1):
            # idx, username, score, duration, created, deleted = row
            username, score = row
            ret_dct[num] = f"{score} {username}"
    return ret_dct


def create_database():
    if os.path.exists(db):
        os.remove(db)

    upd = """
    CREATE TABLE person (
        id integer not null primary key autoincrement unique,
        username varchar(255),
        score integer,
        duration integer,
        created varchar(255),
        deleted varchar(255) default null
        );
    """
    con = sqlite3.connect(db)
    with con:
        con.execute(upd)
    return {"Ok": True}


if __name__ == "__main__":
    print("-" * 20)
    create_database()

    i = 0
    while i < 100:
        update_database(
            username=get_fake_name(3),
            score=get_random_number(),
            duration=get_random_number(1000, 9999),
        )
        i += 1

    delete_database(id=None, username="Jiqite")
    delete_database(id=1)

    ret = read_database()
    print(ret)
