PRODUCTS = {
    1: {
        "name": "Gentle Hydrating Cleanser",
        "price": "₹499",
        "description": "Soft daily cleanser for dry & sensitive skin",
        "image": "images/cleanser.png",
      "category": "Cleanser"

    },
    2: {
        "name": "Acne Control Cleanser",
        "price": "₹549",
        "description": "Controls excess oil and acne",
        "image": "images/acne_control_cleanser.png",
                "category": "Cleanser"

    },
    3: {
        "name": "Niacinamide Serum",
        "price": "₹699",
        "description": "Reduces pores & boosts glow",
        "image": "images/niacinamide_serum.png",
                "category": "Serum"

    },
    4: {
        "name": "Vitamin C Serum",
        "price": "₹799",
        "description": "Brightens skin tone",
        "image": "images/vitamin_c_serum.png",
                "category": "Serum"

    },
    5: {
        "name": "Oil-Free Gel Moisturizer",
        "price": "₹599",
        "description": "Lightweight hydration",
        "image": "images/oil_free_gel_moisturizer.png",
                "category": "Moisturizer"

    },
    6: {
        "name": "Deep Moisture Cream",
        "price": "₹749",
        "description": "Nourishes and restores skin",
        "image": "images/moisture_cream.png",
                "category": "Moisturizer"

    },
    7: {
        "name": "SPF 50+ Sunscreen",
        "price": "₹699",
        "description": "Broad spectrum protection",
        "image": "images/sunscreen_lotion.png",
                "category": "Sunscreen"
    },
    8: {
        "name": "Salicylic Acid Spot Treatment",
        "price": "₹449",
        "description": "Targets acne & reduces redness",
        "image": "images/salicylic_acid.png",
                "category": "Serum"

    }
}


from flask import Flask, render_template, request, jsonify,redirect, url_for, session
import sqlite3
app = Flask(__name__)
app.secret_key = "fia_secret_key"

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- PRODUCTS ----------------
@app.route("/products")
def products():
    category = request.args.get("category")

    if category:
        category = category.lower()   # <-- important safety line
        filtered_products = {
            id: product
            for id, product in PRODUCTS.items()
            if product["category"].lower() == category
            
        }
    else:
        filtered_products = PRODUCTS

    return render_template("products.html", products=filtered_products)
# ---------------- PRODUCT DETAIL ----------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = PRODUCTS.get(product_id)

    if not product:
        return "Product not found", 404

    return render_template(
        "product_detail.html",
        product=product,
        product_id=product_id
    )
# ---------------- CHATBOT ----------------
@app.route("/recommend", methods=["POST"])
def recommend():
    skin_type = request.form.get("skin_type")
    concern = request.form.get("concern")

    recommended_ids = set()   # prevents duplicates

    # ---------------- SKIN TYPE LOGIC ----------------
    if skin_type == "Dry":
        recommended_ids.update([1, 6, 4, 7])

    elif skin_type == "Oily":
        recommended_ids.update([2, 5, 3, 7])

    elif skin_type == "Combination":
        recommended_ids.update([1, 5, 3, 7])

    elif skin_type == "Sensitive":
        recommended_ids.update([1, 6, 7])

    # ---------------- PROBLEM LOGIC ----------------
    if concern == "Acne":
        recommended_ids.update([2, 3, 5, 7])

    elif concern == "Pigmentation":
        recommended_ids.update([4, 3, 7])

    elif concern == "Dark Spots":
        recommended_ids.update([4, 3, 7])

    elif concern == "Dullness":
        recommended_ids.update([4, 1, 6, 7])

    # ---------------- BUILD RESPONSE ----------------
    recommended = []

    for pid in recommended_ids:
        product = PRODUCTS.get(pid)
        if product:
            recommended.append({
                "name": product["name"],
                "url": f"/product/{pid}"
            })

    return jsonify(recommended)

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart
    return redirect(url_for("cart"))
# ---------------- ADD TO CART ----------------
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = PRODUCTS.get(int(pid))
        if product:
            price = int(product["price"].replace("₹", ""))
            subtotal = price * qty
            total += subtotal

            cart_items.append({
                "id": pid,              
                "product": product,
                "quantity": qty,
                "subtotal": subtotal
            })

    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    session["cart"] = cart
    return redirect(url_for("cart"))
@app.route("/increase/<int:product_id>")
def increase(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)
    cart[pid] += 1
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/decrease/<int:product_id>")
def decrease(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if cart[pid] > 1:
        cart[pid] -= 1
    else:
        del cart[pid]

    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- CHECKOUT ----------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    # Build cart items from PRODUCTS dictionary
    for pid, qty in cart.items():
        product = PRODUCTS.get(int(pid))
        if product:
            price = int(product["price"].replace("₹", ""))
            subtotal = price * qty
            total += subtotal

            cart_items.append({
                "id": pid,
                "product": product,
                "quantity": qty,
                "subtotal": subtotal
            })

    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        payment = request.form["payment"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (fullname, email, phone, address, payment, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fullname, email, phone, address, payment, total))

        conn.commit()
        conn.close()

        session.pop("cart", None)

        return redirect(url_for("order_success"))

    return render_template("checkout.html", cart_items=cart_items, total=total)


# ---------------- ORDER SUCCESS ----------------
@app.route("/order_success")
def order_success():
    return render_template("order_success.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()