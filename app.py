
from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error
from sqlalchemy.sql.expression import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


class Users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    surname=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    date_time_of_account_creation=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


class Menu(db.Model):
    menu_id=db.Column(db.Integer,primary_key=True)
    restaurant=db.Column(db.Text,nullable=False)
    product=db.Column(db.Text,nullable=False)
    img_name=db.Column(db.Text,nullable=False)
    img_description=db.Column(db.Text,nullable=False)
    prize=db.Column(db.REAL,nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class Restaurants(db.Model):
    restaurant_id = db.Column(db.Integer,primary_key=True)
    restaurant_name=db.Column(db.String(200),nullable=False)
    restaurant_email=db.Column(db.String(200),nullable=False)
    restaurant_password=db.Column(db.String(200),nullable=False)
    restaurant_phone_number=db.Column(db.Integer,nullable=False)
    restaurant_town=db.Column(db.String(200),nullable=False)
    restaurant_street=db.Column(db.String(200),nullable=False)
    restaurant_home_number=db.Column(db.String(200),nullable=False)
    restaurant_details=db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
class Orders(db.Model):
    order_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id))
    phone_number=db.Column(db.Integer,nullable=False)
    town=db.Column(db.Text,nullable=False)
    street=db.Column(db.Text,nullable=False)
    home_number=db.Column(db.Text,nullable=False)
    details=db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    restaurants = db.session.query(Menu).order_by(func.random()).limit(4).all()
    menu = []
    for item in restaurants:
        menu.append({
            'restaurant': item.restaurant,
            'product': item.product,
            'price': f"{item.prize:.2f} zł",
            'id': item.menu_id,
        })
    return render_template("index.html", menu=menu)

@app.route("/register_restaurant", methods=["GET", "POST"])
def register_restaurant():

    "rejestracja restauracji"
    # Metoda POST
    if request.method == "POST":
        if (not request.form.get("Nazwa") or
                not request.form.get("E-mail") or
                not request.form.get("Haslo") or
                not request.form.get("HasloPowtorz")):
            return error("Wszystkie pola muszą być wypełnione")

        # Sprawdzam czy hasło i potwierdzenie hasła jest poprawne, w przeciwnym razie wyświetlam błąd
        if request.form.get("HasloPowtorz") != request.form.get("Haslo"):
            return error("Hasło musi się zgadzać")

        # Tutaj sprawdzam czy email nie jest zajęty
        restaurant = db.session.query(Restaurants).filter(Restaurants.restaurant_email == request.form.get("E-mail")).first()
        if restaurant:
            return error("Ten adres e-mail jest zajęty!")

        else:
            email = request.form.get("E-mail")
            nazwa = request.form.get("Nazwa")
            haslo = generate_password_hash(request.form.get("Haslo"))

            # dodaje użytkownika do bazy danych

            new_restaurant = Restaurants(restaurant_name=nazwa,
                                         restaurant_email=email,
                                         restaurant_password=haslo,
                                         restaurant_phone_number = '0',
                                         restaurant_town = '0',
                                         restaurant_street = '0',
                                         restaurant_home_number = '0' ,
                                         restaurant_details = '0',
            )
            db.session.add(new_restaurant)
            db.session.commit()

            # Przekierowuje na strone główną
            return render_template("login_restaurant.html")
    else:
        return render_template("register_restaurant.html")
@app.route("/login_restaurant", methods=["GET", "POST"])
def login_restaurant():
    """Logowanie restauracji"""
    session.clear()

    # Metoda POST
    if request.method == "POST":
        # Sprawdzam czy dane zostały podane
        if not request.form.get("E-mail") or not request.form.get("Haslo"):
            return error("Musisz podać e-mail i hasło!")

        # Szukam w bazie czy taki użytkownik istnieje i sprawdzam hasło
        restaurant = db.session.query(Restaurants).filter(Restaurants.restaurant_email == request.form.get("E-mail")).first()
        if not restaurant:
            return error("Niepoprawny e-mail lub hasło!")

        password = check_password_hash(restaurant.restaurant_password, request.form.get("Haslo"))

        if not password:
            return error("Niepoprawny e-mail lub hasło!")

        # Zapamiętuje, że użytkownik jest zalagowany
        user_id = restaurant.restaurant_id
        session["user_id"] = user_id

        # Przekierowuje na strone główną
        return redirect("/")
    else:
        return render_template("login_restaurant.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Logowanie użytkownika"""
    session.clear()

    # Metoda POST
    if request.method == "POST":
        # Sprawdzam czy dane zostały podane
        if not request.form.get("E-mail") or not request.form.get("Haslo"):
            return error("Musisz podać e-mail i hasło!")

        # Szukam w bazie czy taki użytkownik istnieje i sprawdzam hasło
        user = db.session.query(Users).filter(Users.email == request.form.get("E-mail")).first()
        if not user:
            return error("Niepoprawny e-mail lub hasło!")

        password = check_password_hash(user.password, request.form.get("Haslo"))

        if not password:
            return error("Niepoprawny e-mail lub hasło!")

        # Zapamiętuje, że użytkownik jest zalagowany
        user_id = user.user_id
        session["user_id"] = user_id

        # Przekierowuje na strone główną
        return redirect("/")

    # Metoda GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Wylogowanie"""

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])  # metoda GET służy do wyświtlenia strony, a POST, gdy ze strony wysyłane są jakieś informacje do serwera np. formularz
def register():
    """Rejestracja użytkownika"""
    # Metoda POST
    if request.method == "POST":
        # Sprawdzam czy wszytkie wymagane dane zostały podane i czy nie są już zajętę.
        if (not request.form.get("Imie") or
                not request.form.get("Nazwisko") or
                not request.form.get("E-mail") or
                not request.form.get("Haslo") or
                not request.form.get("HasloPowtorz")):
            return error("Wszystkie pola muszą być wypełnione")

        # Sprawdzam czy hasło i potwierdzenie hasła jest poprawne, w przeciwnym razie wyświetlam błąd
        if request.form.get("HasloPowtorz") != request.form.get("Haslo"):
            return error("Hasło musi się zgadzać")

        # Tutaj sprawdzam czy email nie jest zajęty
        user = db.session.query(Users).filter(Users.email == request.form.get("E-mail")).first()
        if user:
            return error("Ten adres e-mail jest zajęty!")

        else:
            email = request.form.get("E-mail")
            imie = request.form.get("Imie")
            nazwisko = request.form.get("Nazwisko")
            haslo = generate_password_hash(request.form.get("Haslo"))

	        # dodaje użytkownika do bazy danych

            new_user = Users(name=imie, surname=nazwisko, email=email,  password=haslo)
            db.session.add(new_user)
            db.session.commit()

	        # Przekierowuje na strone główną
            return render_template("login.html")
    # Tutaj jest metoda GET, czyli wyświetlam template register.html
    else:
        return render_template("register.html")


@app.route("/basket", methods=["POST", "GET"])
def basket():
    if "cart" not in session:
        session["cart"] = []
    if request.method == "POST":
        item_id = request.form.get("id")
        if item_id:
            session["cart"].append(item_id)

    items = []
    it_id = []
    sum = 0
    for i in range(len(session['cart'])):
        query = db.session.query(Menu).filter(Menu.menu_id == session['cart'][i]).first()
        if query:
            it = query.product
            price = query.prize
            sum += price
            items.append(f"{it} - {price}")
            it_id.append(query.menu_id)
    else:
        return render_template("basket.html", items=items, sum=sum, it_id=it_id)


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        item = request.form.get("id")
        session['cart'].remove(item)
        return redirect('/basket')


@app.route("/all_shops")
def all_shops():
    return render_template("all_shops.html")


@app.route("/end")
def end():
    return render_template("end.html")


@app.route("/home_info", methods=["POST", "GET"])
def home_info():
    if request.method == "POST":
        numer_tel = request.form.get("numer_tel")
        miasto = request.form.get("miasto")
        kod_pocztowy = request.form.get("kod_pocztowy")
        ulica = request.form.get("ulica")
        numer_domu = request.form.get("numer_domu")
        szczegoly = request.form.get("szczegoly")

        if (
            not numer_tel
            or not miasto
            or not kod_pocztowy
            or not ulica
            or not numer_domu
            or not szczegoly
        ):
            return error("Wszystkie pola muszą być wypełnione")

        user_id = session.get("user_id")  # Pobieranie user_id z sesji

        new_order = Orders(
            user_id=user_id,
            phone_number=numer_tel,
            town=miasto,
            street=ulica,
            home_number=numer_domu,
            details=szczegoly,
        )
        db.session.add(new_order)
        db.session.commit()

        return redirect("/payment")
    else:
        return render_template("home_info.html")


if __name__ == "__main__":
    app.run(debug=True)

