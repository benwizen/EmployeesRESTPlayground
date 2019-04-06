import sqlite3
from sqlite3 import Error

DB = r"C:\Users\User\PycharmProjects\REST_emp\python_sqlite.db"


def db_conn(db_file):
    return sqlite3.connect(db_file)


def create_connection(db_file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                conn = sqlite3.connect(db_file)
                return func(conn, *args, **kwargs)
            except Error as e:
                print(e)

        return wrapper

    return decorator


@create_connection(DB)
def create_table(conn, table_name, columns):
    try:
        cursor = conn.cursor()
        create_table_stmt = f"create table {table_name} ({', '.join(columns)})"
        cursor.execute(create_table_stmt)
        return {"operation": "create table", "status": "success"}
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def insert(conn, table_name, **kwargs):
    try:
        cursor = conn.cursor()
        data = {k: v for k, v in kwargs.items() if v is not None}
        cols, values = zip(*data.items())
        insert_stmt = f"insert into {table_name} ({', '.join(cols)}) values {values}"
        cursor.execute(insert_stmt)
        conn.commit()
        conn.close()
        return kwargs
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def query(conn, table_name, **kwargs):
    try:
        cursor = conn.cursor()
        select_stmt = f"select * from {table_name}"
        if kwargs:
            predicates = " and ".join((str(k) + '=:' + str(k) for k, v in kwargs.items()))
            select_stmt = f"{select_stmt} where {predicates}"
            res = cursor.execute(select_stmt, kwargs)
        else:
            res = cursor.execute(select_stmt)
        rows = res.fetchall()
        cols = table_columns(table_name)
        return zip_cols_to_rows(cols, rows)
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def delete(conn, table_name, **kwargs):
    try:
        cursor = conn.cursor()
        count_delete = f"select count(*) from {table_name}"
        delete_stmt = f"delete from {table_name}"

        if kwargs:
            data = {k: str(v) for k, v in kwargs.items() if v is not None}
            predicates = " and ".join((str(k) + '=:' + str(k)
                                       if v.lower() != 'null'
                                       else str(k) + ' is null'
                                       for k, v in data.items()))

            count_delete = f"{count_delete} where {predicates}"
            delete_stmt = f"{delete_stmt} where {predicates}"

        count_deleted = cursor.execute(count_delete, kwargs).fetchone()[0]
        cursor.execute(delete_stmt, kwargs)
        conn.commit()
        return f"{count_deleted} rows deleted."
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def update(conn, table_name, changes, who=None):
    if not isinstance(changes, dict) or (who and not isinstance(who, dict)):
        raise Exception(f"changes ({type(changes)}) and who ({type(who)}) arguments must be dictionaries!")
    try:
        cursor = conn.cursor()
        count_update = f"select count(*) from {table_name}"
        changes_str = ", ".join((str(k) + '=:set_' + str(k) for k, v in changes.items()))
        set_args = {'set_' + k: v for k, v in changes.items()}
        update_stmt = f"update {table_name} set {changes_str}"

        if who:
            predicates = " and ".join((str(k) + '=:' + str(k)
                                       if str(v).lower() != 'null'
                                       else str(k) + ' is null'
                                       for k, v in who.items()))

            count_update = f"{count_update} where {predicates}"
            update_stmt = f"{update_stmt} where {predicates}"

        count_updates = cursor.execute(count_update, who).fetchone()[0]
        cursor.execute(update_stmt, {**set_args, **who})
        conn.commit()
        return f"{count_updates} rows updated."
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def all_tables(conn):
    try:
        cursor = conn.cursor()
        query_all_tabs = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
        res = cursor.execute(query_all_tabs)
        return res.fetchall()
    except Error as e:
        return [f"Server ERROR: {e}"]


@create_connection(DB)
def table_columns(conn, table_name):
    import re
    cursor = conn.cursor()
    query_columns = f"select sql from sqlite_master where name='{table_name}';"
    res = cursor.execute(query_columns)
    tab_ddl = res.fetchone()
    match = re.findall(r"\([\w+,?\s?]+\)", tab_ddl[0])
    cols_str = re.sub(r"\(|\)", '', match[0])
    cols = cols_str.split(', ')
    return cols


def zip_cols_to_rows(cols, rows):
    return [dict(zip(cols, row)) for row in rows]


if __name__ == "__main__":
    pass
