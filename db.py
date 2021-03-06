import sqlite3

from network import get_courses, get_name_by_stu_num
from utils import is_stu_num, reply


def update_stu_num(uid, stu_num_arr):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stu WHERE uid = ?', (uid,))
    for stu_num in stu_num_arr:
        cursor.execute('INSERT INTO stu (uid,stu_num) VALUES (?,?)', (uid, stu_num))
    cursor.close()
    conn.commit()
    conn.close()


def create_table(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS stu ('
        'id  INTEGER PRIMARY KEY AUTOINCREMENT ,'
        'uid INTEGER,'
        'stu_num INTEGER'
        ')')


def bind_stu(uid, stu_num_arr):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    create_table(cursor)
    db_stu = get_stu_nums(uid)
    if len(db_stu) == 0:
        for stu in stu_num_arr:
            cursor.execute('INSERT INTO stu (uid,stu_num) VALUES (?,?)', (uid, stu))
        cursor.close()
        conn.commit()
        conn.close()
    else:
        update_stu_num(uid, stu_num_arr)


def get_stu_nums(uid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    create_table(cursor)
    res = list()
    for row in cursor.execute('SELECT stu_num FROM stu WHERE uid = ?', (uid,)):
        res.append(row[0])
    cursor.close()
    conn.commit()
    conn.close()
    return res


def query(stu_ids, offset, update):
    reply_arr = []
    stu_ids = filter(lambda x: is_stu_num(x), stu_ids)
    for stu in stu_ids:
        name = get_name_by_stu_num(int(stu)) if update.message.chat.type == 'private' else '***'
        hint = 'hi~ %s 这里是明天的课表' % (name,) if offset == 1 else 'hi~ %s 这里是今天的课表' % (name,)
        reply_arr.append({'stu_num': stu, 'course': get_courses(stu, offset=offset), 'hint': hint})
    reply(update, reply_arr)
