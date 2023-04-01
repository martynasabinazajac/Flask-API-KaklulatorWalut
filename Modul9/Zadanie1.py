from flask import Flask
from flask import render_template
from flask import request, redirect
import json
import requests
import csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
print(data)

# print(data_rates)

with open("plikzdanymi.csv", 'w') as csvfile:
    fieldnames=['currency', 'code', 'bid', 'ask']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for i in data[0]['rates']:
        writer.writerow(i)
        
#kalkulator
app = Flask(__name__)


@app.route("/kalkulator", methods=['GET', 'POST'])
def calculator():
    rates=data[0]['rates']
    if request.method=='GET':
        items=[i['code'] for i in rates]
        return render_template("kalkulator.html", items=items)
    elif request.method == 'POST':
        waluta=request.form['waluta']
        kwota=request.form['kwota']
        for i in rates:
            waluta== i['code']
            wynik=float(kwota) * (i['bid'])
            print(wynik)
            return f'Wynik: {wynik}'



if __name__ == '__main__':
    app.run(debug=True)