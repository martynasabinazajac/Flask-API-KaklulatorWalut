from flask import Flask
from flask import render_template
from flask import request, redirect
import json
import requests
import csv

# response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
# data = response.json()


#utworzenie pliku csv
def plikcsv():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    with open("plikzdanymi.csv", 'w') as csvfile:
        fieldnames=['currency', 'code', 'bid', 'ask']
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for i in data[0]['rates']:
            writer.writerow(i)

if __name__ == '__main__':
    plikcsv()

#kalkulator
app = Flask(__name__)

def slownik():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates=data[0]['rates']
    rates2={i['code']:i['bid'] for i in rates}
    return rates2



@app.route("/kalkulator", methods=['GET', 'POST'])
def calculator():
    rates3=slownik()
    if request.method=='GET':
        items=[keys for keys in rates3]
        return render_template("kalkulator.html", items=items)
    elif request.method == 'POST':
        waluta=request.form.get("waluta")
        kwota=float(request.form['kwota'])
        waluta2=rates3[waluta]
        wynik= kwota * waluta2
        print(wynik)
        return render_template("kalkulator2.html", wynik=wynik)



if __name__ == '__main__':
    app.run(debug=True)
