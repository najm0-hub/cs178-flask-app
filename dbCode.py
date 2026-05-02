# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def add_user_db(first_name, last_name, genre):
    query = """
    INSERT INTO Users (first_name, last_name, favorite_genre)
    VALUES (%s, %s, %s)
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, (first_name, last_name, genre))
    conn.commit()
    cur.close()
    conn.close()


def get_users_db():
    query = "SELECT * FROM Users"
    return execute_query(query)


def delete_user_db(first_name):
    query = "DELETE FROM Users WHERE first_name = %s"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, (first_name,))
    conn.commit()
    cur.close()
    conn.close()



def get_users_with_movies():
    query = """
    SELECT Users.first_name, Users.last_name, Movies.title
    FROM Users
    JOIN Movies ON Users.favorite_genre = Movies.genre
    """
    return execute_query(query)