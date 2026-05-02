# author: Najmo
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


# shows countries 
@app.route('/countries')
def countries():
    query = "SELECT Name, Continent, Population FROM Country LIMIT 20;"
    data = execute_query(query)
    return render_template('display_users.html', countries=data)


# search countries
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        continent = request.form['continent']

        query = "SELECT Name, Population FROM Country WHERE Continent = %s;"
        data = execute_query(query, (continent,))

        return render_template('display_users.html', countries=data)

    return render_template('add_user.html')  # reuse as search form


# joins
@app.route('/cities', methods=['GET', 'POST'])
def cities():
    if request.method == 'POST':
        country = request.form['country']

        query = """
        SELECT City.Name, Country.Name AS Country
        FROM City
        JOIN Country ON City.CountryCode = Country.Code
        WHERE Country.Name = %s;
        """
        data = execute_query(query, (country,))

        return render_template('display_users.html', countries=data)

    return render_template('delete_user.html')  # reuse as city form



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)