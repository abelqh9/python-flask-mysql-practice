from python_belt_app2 import app
from python_belt_app2.models.user import User
from python_belt_app2.models.car import Car
from flask import render_template, request, redirect, session, flash

# TEMPLATES RENDERING
@app.route("/")
def index():
    # session.clear()
    if "user_id" in session:
        return redirect("/dashboard")
    else:
        return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        cars = Car.get_all_cars()
        seller_names = {}

        for car in cars:
            car_id = car.id
            seller_names[f"{car_id}"] = Car.get_car_seller_name({"car_id": car_id})

        # print(1111111111111111, Car.get_all_cars_sold_ids())
        
        return render_template(
            "dashboard.html",
            user = User.get_user({"user_id": session["user_id"]}),
            cars = cars,
            seller_names = seller_names,
            cars_sold_ids = Car.get_all_cars_sold_ids()
        )
    else:
        return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    if "user_id" in session:
        return render_template(
            "show_user.html",
            user = User.get_user({"user_id": user_id}),
            cars = Car.get_all_cars_of_a_user({"user_id": user_id})
        )
    else:
        return render_template("index.html")

# PROCESSES
@app.route("/register", methods=["POST"])
def register():
    is_valid = True
    form_data = {
        "first_name": request.form["first_name"].strip(),
        "last_name": request.form["last_name"].strip(),
        "email": request.form["email"].strip(),
        "password": request.form["password"].strip(),
        "confirm_password": request.form["confirm_password"].strip()
    }
    # print(form_data)
    if not User.first_name_is_valid(form_data):
        flash("Your first name must be at least 3 characters.", "register_error")
        is_valid = False
    if not User.last_name_is_valid(form_data):
        flash("Your last name must be at least 3 characters.", "register_error")
        is_valid = False
    if not User.email_is_valid(form_data):
        flash("The email must be a valid email.", "register_error")
        is_valid = False
    if User.email_exist(form_data):
        flash("The email alredy exist.", "register_error")
        is_valid = False
    if not User.password_is_valid(form_data):
        flash("The password must be at least 8 characters.", "register_error")
        is_valid = False
    if not form_data['password'] == form_data['confirm_password']:
        flash("Passwords are not the same", "register_error")
        is_valid = False
    if is_valid:
        password_hash = User.create_password(form_data)
        user_id = User.add_user({
            "first_name": form_data["first_name"],
            "last_name": form_data["last_name"],
            "email": form_data["email"],
            "password": password_hash
        })
        # print("Adasdas-dasdasdas", user_id)
        session['user_id'] = user_id
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    is_valid = True
    form_data = {
        "email": request.form["email"].strip(),
        "password": request.form["password"].strip()
    }
    if not User.email_exist(form_data):
        flash("The email does not exist.", "login_error")
        is_valid = False
    elif not User.password_is_correct(form_data):
        flash("Incorrect password.", "login_error")
        is_valid = False
    if is_valid:
        session['user_id'] = User.get_user_id_by_email(form_data)
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")