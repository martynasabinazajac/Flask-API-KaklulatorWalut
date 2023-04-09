from flask import Flask
from flask import render_template
from flask import request, redirect
import json
import requests
import csv

app = Flask(__name__)

# utworzenie pliku csv
def plikcsv(data):
    with open("plikzdanymi.csv", "w") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for i in data[0]["rates"]:
            writer.writerow(i)


# kalkulator
def slownik(data):
    rates = data[0]["rates"]
    rates2 = {i["code"]: i["bid"] for i in rates}
    return rates2


@app.route("/kalkulator", methods=["GET", "POST"])
def calculator():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates3=slownik(data)
    wynik=""
    items = rates3.keys()
    if request.method == "POST":
        waluta = request.form.get("waluta")
        kwota = float(request.form["kwota"])
        waluta2 = rates3[waluta]
        wynik = kwota * waluta2
    return render_template("kalkulator.html", items=items, wynik=wynik)


if __name__ == "__main__":
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    plikcsv(data)
    app.run(debug=True)

