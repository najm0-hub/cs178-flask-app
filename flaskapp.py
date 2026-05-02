# author: Najmo
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT
# description: Country Explorer Flask App using MySQL (world database)
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = "your_secret_key"


# -------------------------
# HOME PAGE
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')


# -------------------------
# SHOW ALL COUNTRIES
# -------------------------
@app.route('/countries')
def countries():
    try:
        query = "SELECT name, iso2 FROM countries LIMIT 50;"
        data = execute_query(query)
        return render_template('countries.html', countries=data)
    except Exception as e:
        return str(e)


# -------------------------
# SEARCH COUNTRIES (BY CONTINENT OR NAME)
# -------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']

        try:
            query = """
            SELECT name, iso2
            FROM countries
            WHERE name LIKE %s
            LIMIT 50;
            """
            data = execute_query(query, (f"%{keyword}%",))
            return render_template('countries.html', countries=data)

        except Exception as e:
            return str(e)

    return render_template('search.html')


# -------------------------
# FIND CITIES BY COUNTRY CODE
# -------------------------
@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        country_code = request.form['country_code']

        try:
            query = """
            SELECT cities.name AS city, countries.name AS country
            FROM cities
            JOIN countries ON cities.country_id = countries.id
            WHERE countries.iso2 = %s
            LIMIT 100;
            """
            data = execute_query(query, (country_code,))
            return render_template('find.html', results=data)

        except Exception as e:
            return str(e)

    return render_template('find.html')


# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)