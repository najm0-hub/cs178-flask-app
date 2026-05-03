# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries

import pymysql
import creds


def get_conn():
    """Create and return a connection to the MySQL RDS instance."""
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )


def execute_query(query, args=()):
    """Execute a SELECT query and return results."""
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(query, args)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return rows


def execute_action(query, args=()):
    """
    Execute INSERT, UPDATE, DELETE queries.
    Commits automatically.
    """
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(query, args)
        conn.commit()
    finally:
        cur.close()
        conn.close()


# -------------------------
# CHINOOK-SPECIFIC FUNCTIONS
# -------------------------

def get_tracks():
    """Get tracks with artist and album (JOIN)."""
    query = """
    SELECT Track.Name AS Track, Artist.Name AS Artist, Album.Title AS Album
    FROM Track
    JOIN Album ON Track.AlbumId = Album.AlbumId
    JOIN Artist ON Album.ArtistId = Artist.ArtistId
    LIMIT 50;
    """
    return execute_query(query)


def search_tracks(keyword):
    """Search tracks by name."""
    query = """
    SELECT Name
    FROM Track
    WHERE Name LIKE %s
    LIMIT 50;
    """
    return execute_query(query, (f"%{keyword}%",))


def get_tracks_by_artist(artist_name):
    """Find tracks by artist (JOIN)."""
    query = """
    SELECT Track.Name AS Track, Artist.Name AS Artist
    FROM Track
    JOIN Album ON Track.AlbumId = Album.AlbumId
    JOIN Artist ON Album.ArtistId = Artist.ArtistId
    WHERE Artist.Name = %s
    LIMIT 50;
    """
    return execute_query(query, (artist_name,))