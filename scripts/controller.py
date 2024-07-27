from scripts.database import Database
from datetime import datetime, timedelta
import re

class Controller:
    '''
    CONTROLLER COMPLETES ALL COMPUTATIONS AND LOGIC FROM QUERY OUTPUTS TO USE IN WEBPAGES
    '''

    def __init__(self):
        self.db = Database()

    def connect_db(self):
        self.db.start_conenction()

    def close_db(self):
        self.db.close_conenction()
        
    """
    USERS/LOGIN/REGISTER PAGE
    """

    def add_user(self, username, hash, email):
        today = datetime.now().date()
        self.db.insert_user(username, hash, today, email)

    def check_username_exists(self, username):
        return len(self.db.get_user_by_name(username)) > 0

    def get_user_by_name(self, username):
        return self.db.get_user_by_name(username)[0]
    
    def get_user_by_id(self, id):
        return self.db.get_user_by_id(int(id))[0]
    
    def insert_goals(self, user_id, weight, calories, carbs, protein, fats):
        today = datetime.now().date()
        self.db.insert_goals(user_id, today, weight, calories, carbs, protein, fats)

    def get_latest_goal(self, user_id):
        return self.db.get_latest_goals(user_id)
    
    def is_valid_email(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email)
    
    def update_profile(self, user_id, username, email):
        self.db.update_user(user_id, username, None, email)
    
    def update_goals(self, user_id, weight, calories, carbs, protein, fats):
        print(user_id, weight, calories, carbs, protein, fats)
        date = datetime.now()
        self.db.insert_goals(user_id, date, weight, calories, carbs, protein, fats)

    """
    FRIENDS PAGE
    """
    
    def add_friend(self, user_id1, user_id2):
        date = datetime.now().date()
        if user_id2 not in self.get_friend_ids(user_id1):
            if self.db.insert_friends(user_id1, user_id2, date):
                return True
        return False
    
    def remove_friend(self, user_id1, user_id2):
        if user_id2 in self.get_friend_ids(user_id1):
            if self.db.remove_friends(user_id1, user_id2):
                return True
        return False

    def get_friend_ids(self, user_id):
        friend_pairs = self.db.get_friends(user_id)
        friends = set()

        for pair in friend_pairs:
            if user_id == pair[0]:
                friends.add(pair[1])
            elif user_id == pair[1]:
                friends.add(pair[0])
        return friends

    def get_friends(self, user_id):
        friends = [self.db.get_user_by_id(friend_id)[0] for friend_id in self.get_friend_ids(user_id)]
        return [{"id":friend[0], "name":friend[2], "email":friend[4], "date_added":self.get_date_added(friend[0], user_id)} for friend in friends]
    
    def get_all_users(self, user_id):
        all_users = self.db.get_all_users()
        return [{"name":user[2], "email":user[4]} for user in all_users if user[0] != user_id]
    
    def get_all_available_users(self, user_id):
        all_users = self.get_all_users(user_id)
        return [user for user in all_users if user["name"] not in [friend["name"] for friend in self.get_friends(user_id)]]
    
    def get_date_added(self, user_id1, user_id2):
        return self.db.get_friend_pair(user_id1, user_id2)[2]

    """
    MEALS PAGE
    """
    
    def get_food_id(self, name):
        return self.db.get_food_by_name(name)[0][0]
    
    def get_food(self, name):
        return self.db.get_food_by_name(name)
    
    def get_all_foods(self):
        all_foods = self.db.get_all_foods()
        return [food[1] for food in all_foods]
    
    def add_meal(self, user_id, food_id, datetime, classification, filepath):
        self.db.insert_meals(user_id, food_id, datetime, classification, filepath)
    
    def update_meal(self, user_id, food_id, datetime, classification, filepath):
        self.db.update_meals(food_id, user_id, datetime, classification, filepath)

    def remove_meal(self, user_id, date, classification):
        self.db.remove_meals(user_id, date, classification)
    
    def get_meals(self, user_id):
        today = datetime.today().date()
        all_meals = {}
        date_joined = self.db.get_date_joined(user_id)[0][0]
        counter = 1
        
        while str(today + timedelta(days=1)) != date_joined:
            all_meals[today] = {}
            meals = self.db.get_meals(user_id, today)

            all_meals[today]["meals"] = {}
            
            for meal in meals:
                _, food_id, _, classification, _ = meal
                individual_meal = {}
                individual_meal["meal_details"] = meal
                individual_meal["meal_name"], individual_meal["calories"], individual_meal["carbs"], individual_meal["protein"], individual_meal["fats"] = self.get_meal_nutrition(food_id)
                all_meals[today]["meals"][classification] = individual_meal

            all_meals[today]["daily_nutrition"] = {}
            all_meals[today]["daily_nutrition"]["calories"], all_meals[today]["daily_nutrition"]["carbs"], all_meals[today]["daily_nutrition"]["protein"], all_meals[today]["daily_nutrition"]["fats"] = self.sum_meal_nutrition(meals)
            all_meals[today]["counter"] = counter
            today -= timedelta(days=1)
            counter += 1
        return all_meals
    
    def get_meal_nutrition(self, food_id):
        food = self.db.get_food_by_id(food_id)[0]
        return food[1], food[2], food[3], food[4], food[5]

    def sum_meal_nutrition(self, meals):
        daily_calories = daily_carbs = daily_protein = daily_fats = 0.0
        for meal in meals:
            _, meal_calories, meal_carbs, meal_protein, meal_fats = self.get_meal_nutrition(meal[1])

            daily_calories += meal_calories
            daily_carbs += meal_carbs
            daily_protein += meal_protein
            daily_fats += meal_fats
        return daily_calories, daily_carbs, daily_protein, daily_fats

    """
    DASHBOARD PAGE
    """
    
    def get_weights(self, user_id):
        cur_month = datetime.today().date()
        starting_period = cur_month - timedelta(days=6 * 30)
        updates = self.db.get_body_updates(starting_period, user_id)
        
        weights, dates = [update[2] for update in updates], [update[1] for update in updates]
        return weights, dates
    
    def add_weights(self, user_id, weight):
        today = datetime.now().date()
        _, dates = self.get_weights(user_id)
        if str(today) not in dates:
            self.db.insert_body_updates(user_id, today, weight)
    
    def edit_weights(self, user_id, weight):
        today = datetime.now().date()
        _, dates = self.get_weights(user_id)
        if today not in dates:
            self.db.edit_body_updates(user_id, today, weight)

    def get_weight_goal(self, user_id):
        if len(self.db.get_latest_goals(user_id)) > 0:
            return self.db.get_latest_goals(user_id)[0][2]
        return None
    
    def get_calorie_goal(self, user_id):
        if len(self.db.get_latest_goals(user_id)) > 0:
            return self.db.get_latest_goals(user_id)[0][3]
        return None

    def get_nutrition_goals(self, user_id):
        if len(self.db.get_latest_goals(user_id)) > 0:
            return self.db.get_latest_goals(user_id)[0]
        return None
    
    def process_nutrition_goals(self, user_id):
        nutrition_goals = self.get_nutrition_goals(user_id)
        return {"calories":nutrition_goals[3], "carbs":nutrition_goals[4], "protein":nutrition_goals[5], "fats":nutrition_goals[6]}
    
    def get_weekly_food_values(self, user_id):
        today = datetime.today().date()
        calories, carbs, protein, fats, dates = [], [], [], [], []

        for _ in range(7):
            meals = self.db.get_meals(user_id, today)
            daily_calories, daily_carbs, daily_protein, daily_fats = self.sum_meal_nutrition(meals)

            calories.append(daily_calories)
            carbs.append(daily_carbs)
            protein.append(daily_protein)
            fats.append(daily_fats)
            dates.append(today)
            today -= timedelta(days=1)
            
        return calories[::-1], carbs[::-1], protein[::-1], fats[::-1], dates[::-1]
    
    def get_cur_nutrition_values(self, user_id):
        _, carbs, protein, fats, dates = self.get_weekly_food_values(user_id)
        idx = dates.index(max(dates))
        return carbs[idx], protein[idx], fats[idx]
    
    def get_cur_nutrition_percentage(self, user_id):
        goals = self.process_nutrition_goals(user_id)
        if not goals:
            return None, None, None
        
        carbs_goals, protein_goals, fats_goals = goals.get("carbs"), goals.get("protein"), goals.get("fats")
        carbs_today, protein_today, fats_today = self.get_cur_nutrition_values(user_id)
        print(carbs_today, carbs_goals, protein_today, protein_goals, fats_today, fats_goals)
        return round(carbs_today / carbs_goals * 100), round(protein_today / protein_goals * 100), round(fats_today / fats_goals * 100)

    def get_weekly_nutrition_percentage(self, user_id):
        _, carbs, protein, fats, _ = self.get_weekly_food_values(user_id)
        carbs_weekly, protein_weekly, fats_weekly = sum(carbs) / 7, sum(protein) / 7, sum(fats) / 7

        goals = self.process_nutrition_goals(user_id)
        if not goals:
            return None, None, None
        carbs_goals, protein_goals, fats_goals = goals.get("carbs"), goals.get("protein"), goals.get("fats")

        return round(carbs_weekly / carbs_goals * 100), round(protein_weekly / protein_goals * 100), round(fats_weekly / fats_goals * 100)

    def get_weekly_avg_nutrition(self, user_id):
        _, carbs, protein, fats, dates = self.get_weekly_food_values(user_id)
        num_days = len(dates)

        avg_carbs = round(sum(carbs) / num_days, 1)
        avg_protein = round(sum(protein) / num_days, 1)
        avg_fats = round(sum(fats) / num_days, 1)

        return avg_carbs, avg_protein, avg_fats
    
    def today_added_weight(self, user_id):
        today = datetime.now().date()
        _, dates = self.get_weights(user_id)
        return str(today) in dates