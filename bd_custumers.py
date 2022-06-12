import sqlite3


def start_bd():
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
       custid INT PRIMARY KEY,
       fio TEXT,
       tel TEXT,
       tgid TEXT,
       adress TEXT);
    """)
    conn.commit()
    conn.close()


def insert_customer(cust):
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO customers
                              (custid, fio, tel, tgid, adress)
                              VALUES (NULL, ?, ?, ?, ?);""", cust)
    conn.commit()
    conn.close()


def input_all():
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from customers"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    print("Всего строк:  ", len(records))
    for row in records:
        print("custid:", row[0])
        print("fio:", row[1])
        print("tel:", row[2])
        print("tgid:", row[3])
        print("adress:", row[4])
    conn.close()


def take_customer(id):
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from customers WHERE tgid = '""" + str(id) + """'"""
    print(sqlite_select_query)
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records


def edit_customer(name_st, id, new_data):
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    if name_st == 'fio':
        sqlite_update_query = """UPDATE customers SET fio = '""" + str(new_data) + """' WHERE tgid = '""" + str(id) + """'"""
        print(sqlite_update_query)
        cur.execute(sqlite_update_query)
        conn.commit()
        conn.close()
    elif name_st == 'tel':
        sqlite_update_query = """UPDATE customers SET tel = '""" + str(new_data) + """' WHERE tgid = '""" + str(id) + """'"""
        print(sqlite_update_query)
        cur.execute(sqlite_update_query)
        conn.commit()
        conn.close()
    elif name_st == 'adress':
        sqlite_update_query = """UPDATE customers SET adress = '""" + str(new_data) + """' WHERE tgid = '""" + str(
            id) + """'"""
        print(sqlite_update_query)
        cur.execute(sqlite_update_query)
        conn.commit()
        conn.close()