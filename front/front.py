from flask import Flask, render_template
import data

app = Flask(__name__)


@app.route("/")
def index():
    produits = data.get_products_3_last_movements()
    print("recupération ds produits", len(produits))
    return render_template("stock_produits.html", produits=produits)


if __name__ == "__main__":
    app.run(debug=True)
