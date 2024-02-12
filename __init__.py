from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/commits.html/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Création d'une DataFrame pour le traitement
    data = {
        'timestamp': [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') for commit in commits_data]
    }
    df = pd.DataFrame(data)

    # Grouper par minute et compter les commits
    df.set_index('timestamp', inplace=True)
    commits_per_minute = df.resample('T').size()

    # Préparer les données pour le graphique
    times = commits_per_minute.index.strftime('%Y-%m-%d %H:%M')
    counts = commits_per_minute.values

    # Renvoyer le template HTML avec les données pour le graphique
    return render_template('commits.html', times=times, counts=counts)

if __name__ == "__main__":
    app.run(debug=True)

  
if __name__ == "__main__":
  app.run(debug=True)

