import sqlite3


def update_stu_num(uid, stu_num):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stu WHERE uid = ?', (uid,))
    cursor.execute('UPDATE stu SET stu_num = ? WHERE uid= ?', (stu_num, uid))
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


def bind_stu(uid, stu_num):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    create_table(cursor)
    db_stu = get_stu_nums(uid)
    if len(db_stu) == 0:
        for stu in stu_num:
            cursor.execute('INSERT INTO stu (uid,stu_num) VALUES (?,?)', (uid, stu))
        cursor.close()
        conn.commit()
        conn.close()
    else:
        update_stu_num(uid, stu_num)


def get_stu_nums(uid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    create_table(cursor)
    res = []
    for row in cursor.execute('SELECT stu_num FROM stu WHERE uid = ?', (uid,)):
        res = res.append(row)
        break
    cursor.close()
    conn.commit()
    conn.close()
    return res
