# author: Najmo
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = "your_secret_key"


# -------------------------
# HOME
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')


# -------------------------
# VIEW TRACKS (JOIN!)
# -------------------------
@app.route('/tracks')
def tracks():
    try:
        query = """
        SELECT Track.Name AS Track, Artist.Name AS Artist, Album.Title AS Album
        FROM Track
        JOIN Album ON Track.AlbumId = Album.AlbumId
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        LIMIT 50;
        """
        data = get_tracks()
        return render_template('tracks.html', tracks=data)
    except Exception as e:
        return str(e)


# -------------------------
# SEARCH TRACKS
# -------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']

        try:
            query = """
            SELECT Name
            FROM Track
            WHERE Name LIKE %s
            LIMIT 50;
            """
            data = get_tracks(query, (f"%{keyword}%",))
            return render_template('tracks.html', tracks=data)

        except Exception as e:
            return str(e)

    return render_template('search.html')


# -------------------------
# FIND TRACKS BY ARTIST
# -------------------------
@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        artist = request.form['artist']

        try:
            query = """
            SELECT Track.Name AS Track, Artist.Name AS Artist
            FROM Track
            JOIN Album ON Track.AlbumId = Album.AlbumId
            JOIN Artist ON Album.ArtistId = Artist.ArtistId
            WHERE Artist.Name = %s;
            """
            data = get_tracks(query, (artist,))
            return render_template('find.html', results=data)

        except Exception as e:
            return str(e)

    return render_template('find.html')


# -------------------------
# RUN
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)