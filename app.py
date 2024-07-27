import os
import datetime

from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from scripts.controller import Controller
from scripts.helper import login_required, apology

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
Accounts
    - register
    - login
    - logout
    - goals
    - edit_profile
"""

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        controller = Controller()
        controller.connect_db()

        username = request.form.get("username").upper()
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirm-password")

        # Checks if username is submitted
        if not username:
            flash("Please enter a valid username.")
            return render_template("register.html")
        # Checks if username exists
        if controller.check_username_exists(username):
            flash("Username is taken. Please choose a new one.")
            return render_template("register.html")
        # Checks if password is submitted
        if not email or not controller.is_valid_email(email):
            flash("Please enter a valid email.")
            return render_template("register.html")
        if not password:
            flash("Please enter a password.")
            return render_template("register.html")
        # Checks if password has been confirmed
        if not confirmation:
            flash("Please confirm your password.")
            return render_template("register.html")
        # Checks if password and confirmation password match
        if password != confirmation:
            flash("Please ensure your password and confirmation password match.")
            return render_template("register.html")

        hash = generate_password_hash(password)
        controller.add_user(username, hash, email)

        return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')
    else:
        controller = Controller()
        controller.connect_db()

        username = request.form.get("username").upper()
        password = request.form.get("password")

        # Checks if username is submitted and ensures it exists
        if not username:
            flash("Please enter a valid username.")
            return render_template('login.html')
        # Checks if password is submitted
        if not password:
            flash("Please enter password.")
            return render_template('login.html')
        if not controller.check_username_exists(username):
            flash("User does not exist.")
            return render_template('login.html')

        user = controller.get_user_by_name(username)
        user_id, hash = user[0], user[1]

        # Ensures correct password
        if not check_password_hash(hash, password):  
            flash("Incorrect password.")
            return render_template('login.html')

        # Remember which user has logged in
        session["user_id"] = user_id

        if len(controller.get_latest_goal(user_id)) > 0:
            return redirect('/dashboard')
        return redirect('/goals')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/goals", methods=["GET", "POST"])
def goals():
    if request.method == "GET":
        return render_template('goals.html')
    else:
        controller = Controller()
        controller.connect_db()

        user_id = session.get("user_id")

        weight = request.form.get("target-weight")
        calories = request.form.get("target-calories")
        carbs = request.form.get("target-carbs")
        protein = request.form.get("target-protein")
        fats = request.form.get("target-fats")

        if not weight:
            flash("Please enter your target weight (kg).")
            return redirect("/goals")
        elif not calories:
            flash("Please enter your target calorie intake (Kcal).")
            return redirect("/goals")
        elif not carbs:
            flash("Please enter your target carbs intake (g).")
            return redirect("/goals")
        elif not protein:
            flash("Please enter your target protein intake (g).")
            return redirect("/goals")
        elif not fats:
            flash("Please enter your target fats intake (g).")
            return redirect("/goals")
        
        controller.insert_goals(user_id, weight, calories, carbs, protein, fats)

        return redirect('/dashboard')
    
@app.route('/edit_profile', methods=["POST"])
def edit_profile():
    controller = Controller()
    controller.connect_db()

    user_id = session.get("user_id")

    username = request.form.get("edit-profile-name")
    email = request.form.get("edit-profile-email")

    if not username:
        flash("Please enter a valid username.")
        return redirect('/dashboard')
    if not email or not controller.is_valid_email(email):
        flash("Please enter a valid email.")
        return redirect('/dashboard')
    
    if controller.check_username_exists(username):
        username = controller.get_user_by_id(user_id)[2]
    
    weight = request.form.get("edit-target-weight")
    calories = request.form.get("edit-target-calories")
    carbs = request.form.get("edit-target-carbs")
    protein = request.form.get("edit-target-protein")
    fats = request.form.get("edit-target-fats")

    if not weight:
        flash("Please enter your target weight (kg).")
        return redirect('/dashboard')
    elif not calories:
        flash("Please enter your target calorie intake (Kcal).")
        return redirect('/dashboard')
    elif not carbs:
        flash("Please enter your target carbs intake (g).")
        return redirect('/dashboard')
    elif not protein:
        flash("Please enter your target protein intake (g).")
        return redirect('/dashboard')
    elif not fats:
        flash("Please enter your target fats intake (g).")
        return redirect('/dashboard')

    controller.update_profile(user_id, username, email)
    controller.update_goals(user_id, weight, calories, carbs, protein, fats)
    
    return redirect('/dashboard')

"""
Dashboard
    - dashboard
    - update_weights
    - update_calories
    - update_nutrition
    - add_weights
"""

@app.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    controller = Controller()
    controller.connect_db()

    user_id = session.get("user_id")

    _, _, username, birthday, email, joined, filepath = controller.get_user_by_id(int(user_id))
    goals = controller.get_latest_goal(user_id)[0]
    friends = len(controller.get_friends(user_id))
    user = {"email":email, "username":username, "birthday":birthday, "joined":joined, "filepath":filepath, "friends":friends, "weight_goal":goals[2], "calorie_goal":goals[3], "carbs_goal":goals[4], "protein_goal":goals[5],"fats_goal":goals[6]}

    weights, dates = controller.get_weights(user_id)
    weight_goal = controller.get_weight_goal(user_id)
    weight_chart_values = {"weights": weights, "dates": dates, "goal": weight_goal}

    today_added = controller.today_added_weight(user_id)

    calories, _, _, _, dates = controller.get_weekly_food_values(user_id)
    calorie_goal = controller.get_calorie_goal(user_id)
    calorie_chart_values = {"calories": calories, "dates": dates, "goal": calorie_goal}
    
    carbs_percentage, protein_percentage, fats_percentage = controller.get_weekly_nutrition_percentage(user_id)
    carbs_avg, protein_avg, fats_avg = controller.get_weekly_avg_nutrition(user_id)
    nutrition_chart_values = {"carbs":{"average":carbs_avg, "percentage":carbs_percentage}, "protein":{"average":protein_avg, "percentage":protein_percentage}, "fats":{"average":fats_avg, "percentage":fats_percentage}}

    return render_template('dashboard.html', today_added=today_added, user=user, nutrition_chart_values=nutrition_chart_values, calorie_chart_values=calorie_chart_values, weight_chart_values=weight_chart_values)

@app.route('/add_weights', methods=["POST"])
def add_weights():
    controller = Controller()
    controller.connect_db()

    user_id = session.get("user_id")

    weight = request.form.get("today-weight-value")
    if not weight:
        flash("Please submit a value (kg).")
        return redirect('/dashboard')
    try:
        weight = int(weight)
    except Exception as e:
        flash("Please enter a valid weight value.")

    controller.add_weights(user_id, weight)

    return redirect('/dashboard')

@app.route('/edit_weights', methods=["POST"])
def edit_weights():
    controller = Controller()
    controller.connect_db()

    user_id = session.get("user_id")

    weight = request.form.get("today-weight-value")
    if not weight:
        flash("Please submit a value (kg).")
        return redirect('/dashboard')
    try:
        weight = int(weight)
    except Exception as e:
        flash("Please enter a valid weight value.")

    controller.edit_weights(user_id, weight)

    return redirect('/dashboard')

"""
Meals
    - meals
    - update_food_names
    - add_meal
    - update_meal
"""

@app.route('/meals', methods=["GET"])
@login_required
def meals():
    controller = Controller()
    controller.connect_db()

    user_id = session.get("user_id")

    _, _, username, birthday, email, joined, filepath = controller.get_user_by_id(int(user_id))
    friends = len(controller.get_friends(user_id))
    user = {"email":email, "username":username, "birthday":birthday, "joined":joined, "filepath":filepath, "friends":friends}

    all_meals = controller.get_meals(user_id)
    food_names = controller.get_all_foods()
    nutrition_goals = controller.process_nutrition_goals(user_id)
    
    return render_template('meals.html', user=user, all_meals=all_meals, food_names=food_names, nutrition_goals=nutrition_goals)

@app.route('/add_meal', methods=["POST"])
def add_meal():
    controller = Controller()
    controller.connect_db()
    
    user_id = session.get("user_id")

    date = request.form.get("meal-date")
    classification = request.form.get("meal-classification")
    meal_name = request.form.get("meal-name")
    filepath = request.form.get("meal-filepath")

    action_type = request.form.get("action-type")

    if not meal_name:
        flash("Please enter a meal name.")
        return redirect("/meals")

    meal_id = controller.get_food_id(meal_name)
    
    if action_type == 'Add':
        controller.add_meal(user_id, meal_id, date, classification, filepath)
    else:
        controller.update_meal(user_id, meal_id, date, classification, filepath)

    return redirect("/meals")

@app.route('/remove_meal', methods=["POST"])
def remove_meal():
    controller = Controller()
    controller.connect_db()
    
    user_id = session.get("user_id")

    date = request.form.get("remove-meal-date")
    classification = request.form.get("remove-meal-classification")

    controller.remove_meal(user_id, date, classification)

    return redirect("/meals")

"""
Friends
    - friends
    - add_friend
    - get_friends
"""

@app.route('/friends', methods=["GET"])
@login_required
def friends():
    controller = Controller()
    controller.connect_db()
    
    user_id = session.get("user_id")

    _, _, username, birthday, email, joined, filepath = controller.get_user_by_id(int(user_id))
    friends = len(controller.get_friends(user_id))
    user = {"email":email, "username":username, "birthday":birthday, "joined":joined, "filepath":filepath, "friends":friends}

    friends = controller.get_friends(user_id)

    users = controller.get_all_available_users(user_id)
    
    return render_template('friends.html', user=user, friends=friends, users=users)

@app.route('/add_friend', methods=["POST"])
def add_friend():
    controller = Controller()
    controller.connect_db()
    
    user1_id = session.get("user_id")

    user2_name = request.form.get("profile-name")

    if not user2_name:
        flash("Please submit a valid account.")
        return redirect('/friends')
    
    user2_id = controller.get_user_by_name(user2_name)[0]

    if user1_id == user2_id:
        flash("You cannot add yourself as a friend.")
        return redirect('/friends')
    
    flash("Unable to add friend. Please try again later.") if not controller.add_friend(user1_id, user2_id) else flash("Friend added!")
    return redirect('/friends')

@app.route('/remove_friend', methods=["POST"])
def remove_friend():
    controller = Controller()
    controller.connect_db()
    
    user1_id = session.get("user_id")

    user2_name = request.form.get("profile-name")

    if not user2_name:
        flash("Please submit a valid account.")
        return redirect('/friends')
    
    user2_id = controller.get_user_by_name(user2_name)[0]

    if user1_id == user2_id:
        flash("You cannot remove yourself as a friend.")
        return redirect('/friends')
    
    flash("Friend removed!") if not controller.remove_friend(user1_id, user2_id) else flash("Unable to remove friend. Please try again later.")
    return redirect('/friends')