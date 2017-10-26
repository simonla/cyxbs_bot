import sqlite3


def update_stu_num(uid, stu_num):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE stu SET stu_num = ? WHERE chat_id = ?', (stu_num, uid))
    cursor.close()
    conn.commit()
    conn.close()


def bind_stu(uid, stu_num):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS stu (chat_id INT (20) PRIMARY KEY , stu_num INT (20))')
    if get_stu_num(uid) is None:
        cursor.execute('INSERT INTO stu (chat_id,stu_num) VALUES (?,?)', (uid, stu_num))
        cursor.close()
        conn.commit()
        conn.close()
    if get_stu_num(uid) != stu_num:
        update_stu_num(uid, stu_num)


def get_stu_num(uid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    res = None
    for row in cursor.execute('SELECT stu_num FROM stu WHERE chat_id = ?', (uid,)):
        res = row[0]
        break
    cursor.close()
    conn.commit()
    conn.close()
    return res
