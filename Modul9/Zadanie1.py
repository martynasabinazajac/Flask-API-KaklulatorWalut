from flask import Flask
from flask import render_template
from flask import request, redirect
import json
import requests
import csv


def DATA():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data


# utworzenie pliku csv
def plikcsv():
    with open("plikzdanymi.csv", "w") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for i in data[0]["rates"]:
            writer.writerow(i)


# kalkulator
app = Flask(__name__)


def slownik():
    rates = data[0]["rates"]
    rates2 = {i["code"]: i["bid"] for i in rates}
    return rates2


@app.route("/kalkulator", methods=["GET", "POST"])
def calculator():
    rates3 = slownik()
    items = rates3.keys()
    if request.method == "POST":
        waluta = request.form.get("waluta")
        kwota = float(request.form["kwota"])
        waluta2 = rates3[waluta]
        wynik = kwota * waluta2
        return render_template("kalkulator.html", wynik=wynik)
    return render_template("kalkulator.html", items=items)


if __name__ == "__main__":
    data = DATA()
    plikcsv()
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    app.run(debug=True)
