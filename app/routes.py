from app import app
from flask import render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
from . import utils

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method=='POST':
        product_id = request.form.get('product_id')
        url = f"https://www.ceneo.pl/{product_id}"
        response = requests.get(url)
        if response.status_code== requests.codes['ok']:
            page_dom= BeautifulSoup(response.text,"html.parser")
            opinions_count = utils.extract(page_dom , 'a.product-review__link > span')
            if opinions_count:
                return redirect(url_for('product', product_id=product_id))
            return render_template("extract.html", error="Podany produkt nie ma żadnych opinii")
        return render_template("extract.html", error="Produkt o takim kodzie nie istnieje")
    return render_template("extract.html")
    

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html", product_id=product_id)