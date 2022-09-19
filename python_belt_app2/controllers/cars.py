from python_belt_app2 import app
from python_belt_app2.models.car import Car
from python_belt_app2.models.user import User
from flask import render_template, request, redirect, session, flash
import datetime

# TEMPLATES RENDERING
@app.route("/cars/<car_id>")
def show_show(car_id):
    if "user_id" in session:
        car = Car.get_car({"car_id": car_id})
        car.format_car_price()
            
        return render_template(
            "show_car.html",
            user = User.get_user({"user_id": session["user_id"]}),
            car = car,
            seller_name = Car.get_car_seller_name({"car_id": car_id}),
        )
    else:
        return redirect("/")

@app.route("/new")
def new_car():
    if "user_id" in session:
        return render_template("new_car.html", user = User.get_user({"user_id": session["user_id"]}),)
    else:
        return redirect("/")

@app.route("/edit/<car_id>")
def edit_show(car_id):
    if "user_id" in session:
        return render_template(
            "edit_car.html",
            user = User.get_user({"user_id": session["user_id"]}),
            car = Car.get_car({"car_id": car_id})
        )
    else:
        return redirect("/")

# PROCESSES
@app.route("/new/process", methods=["POST"])
def new_show_process():
    if "user_id" in session:
        is_valid = True
        data = {
            "price": request.form["price"],
            "model": request.form["model"].strip(),
            "make": request.form["make"].strip(),
            "year": request.form["year"],
            "description": request.form["description"].strip(),
            "user_id": session["user_id"]
        }
        if not Car.price_is_valid(data):
            flash("The price must be grater than 0.")
            is_valid = False
        if not Car.model_is_valid(data):
            flash("The model is required.")
            is_valid = False
        if not Car.make_is_valid(data):
            flash("The make is required.")
            is_valid = False
        if not Car.year_is_valid(data):
            flash("The year must be grater than 0.")
            is_valid = False
        if not Car.description_is_valid(data):
            flash("The description is required.")
            is_valid = False

        if is_valid:
            # print("---------------------", data)
            data["year"] = datetime.datetime(int(data["year"]), 1, 1) 
            Car.add_car(data)
            return redirect("/dashboard")
        else:
            return redirect("/new")
    else:
        return redirect("/")

@app.route("/edit/process", methods=["POST"])
def edit_car_process():
    if "user_id" in session:
        is_valid = True
        data = {
            "price": request.form["price"],
            "model": request.form["model"].strip(),
            "make": request.form["make"].strip(),
            "year": request.form["year"],
            "description": request.form["description"].strip(),
            "car_id": request.form["car_id"]
        }
        # print("xxxxxxxx", data)
        if not Car.price_is_valid(data):
            flash("The price must be grater than 0.")
            is_valid = False
        if not Car.model_is_valid(data):
            flash("The model is required.")
            is_valid = False
        if not Car.make_is_valid(data):
            flash("The make is required.")
            is_valid = False
        if not Car.year_is_valid(data):
            flash("The year must be grater than 0.")
            is_valid = False
        if not Car.description_is_valid(data):
            flash("The description is required.")
            is_valid = False

        if is_valid:
            data["year"] = datetime.datetime(int(data["year"]), 1, 1) 
            Car.edit_car(data)
            return redirect("/dashboard")
        else:
            return redirect("/edit/"+str(request.form["car_id"]))
    else:
        return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    if "user_id" in session:
        Car.delete_car({"car_id": request.form["car_id"]})
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/purchase", methods=["POST"])
def purchase():
    if "user_id" in session:
        Car.add_purchase({
            "user_id": session["user_id"],
            "car_id": int(request.form["car_id"])
        })
        return redirect("/dashboard")
    else:
        return redirect("/")