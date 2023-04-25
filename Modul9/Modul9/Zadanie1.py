from flask import Flask
from flask import render_template
from flask import request, redirect
import json
import requests
import csv

app = Flask(__name__)


def pobieranie_danych():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data


# utworzenie pliku csv
def plikcsv(pobrane):
    with open("plikzdanymi.csv", "w") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for i in pobrane[0]["rates"]:
            writer.writerow(i)


# kalkulator
@app.route("/kalkulator", methods=["GET", "POST"])
def calculator():
    dane = pobieranie_danych()
    rates = dane[0]["rates"]
    rates3 = {i["code"]: i["bid"] for i in rates}
    wynik = ""
    items = rates3.keys()
    if request.method == "POST":
        waluta = request.form.get("waluta")
        kwota = float(request.form["kwota"])
        waluta2 = rates3[waluta]
        wynik = kwota * waluta2
    return render_template("kalkulator.html", items=items, wynik=wynik)


if __name__ == "__main__":
    pobrane = pobieranie_danych()
    app.run(debug=True)
