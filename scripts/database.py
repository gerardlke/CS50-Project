import sqlite3

class Database:
    """
    DATABASE INTERACTS DIRECTLY WITH project.db THROUGH THE QUERIES AND DOES NOT PERFORM ANY FURTHER COMPUTATIONS
    """
    def __init__(self):
        self.sqliteConnection = None
        self.cursor = None

    def start_conenction(self):
        self.sqliteConnection = sqlite3.connect('project.db')
        self.cursor = self.sqliteConnection.cursor()

    def close_conenction(self):
        if self.sqliteConnection:
            self.sqliteConnection.close()
            self.sqliteConnection = None
            self.cursor = None

    def execute_insert(self, query, args):
        try: 
            self.cursor.execute(query, args)
            self.sqliteConnection.commit()
        except sqlite3.Error as e:
            print("Error during INSERT database operation:", e)

    def execute_select(self, query, args):
        try: 
            cursor = self.cursor.execute(query, args)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print("Error during SELECT database operation:", e)

    def execute_update(self, query, args):
        try: 
            self.cursor.execute(query, args)
            self.sqliteConnection.commit()
        except sqlite3.Error as e:
            print("Error during UPDATE database operation:", e)

    def execute_delete(self, query, args):
        try: 
            self.cursor.execute(query, args)
            self.sqliteConnection.commit()
        except sqlite3.Error as e:
            print("Error during DELETE database operation:", e)
            
    """
    USERS TABLE
    """

    def insert_user(self, username, hash, date, email):
        self.execute_insert("INSERT INTO users (username, hash, joined, email) VALUES(?, ?, ?, ?)", (username, hash, date, email))

    def get_user_by_id(self, user_id):
        return self.execute_select("SELECT * FROM users WHERE id = ?", (user_id,))
    
    def get_user_by_name(self, username):
        return self.execute_select("SELECT * FROM users WHERE username = ?", (username,))

    def update_user(self, user_id, username, birthday, email):
        self.execute_update("UPDATE users SET username = ?, birthday = ?, email = ? WHERE id = ?", (username, birthday, email, user_id))

    def get_date_joined(self, user_id):
        return self.execute_select("SELECT joined FROM users WHERE id = ?", (user_id,))
    
    def get_all_users(self):
        return self.execute_select("SELECT * FROM users", ())
    
    """
    FRIENDS TABLE
    """
    
    def insert_friends(self, user_id1, user_id2, date):
        self.execute_insert("INSERT INTO friends (users_id1, users_id2, datetime) VALUES(?, ?, ?)", (user_id1, user_id2, date))

    def remove_friends(self, user_id1, user_id2):
        self.cursor.execute("DELETE FROM friends WHERE (users_id1 = ? AND users_id2 = ?) OR (users_id1 = ? AND users_id2 = ?)", (user_id1, user_id2, user_id2, user_id1))
        self.sqliteConnection.commit()

    def get_friends(self, user_id):
        return self.execute_select("SELECT * FROM friends WHERE users_id1 = ? OR users_id2 = ?", (user_id, user_id))
    
    def get_friend_pair(self, user_id1, user_id2):
        return self.execute_select("SELECT * FROM friends WHERE (users_id1 = ? AND users_id2 = ?) OR (users_id1 = ? AND users_id2 = ?)", (user_id1, user_id2, user_id2, user_id1))[0]

    """
    MEALS TABLE
    """
    
    def insert_meals(self, user_id, food_id, datetime, classification, filepath):
        self.execute_insert("INSERT INTO meals (users_id, food_id, datetime, classification, filepath) VALUES(?, ?, ?, ?, ?)", (user_id, food_id, datetime, classification, filepath))

    def update_meals(self, new_food_id, user_id, datetime, classification, filepath):
        self.execute_update("UPDATE meals SET food_id = ?, filepath = ? WHERE users_id = ? AND datetime = ? AND classification = ?", (new_food_id, filepath, user_id, datetime, classification))

    def get_meals(self, user_id, date):
        return self.execute_select("SELECT * FROM meals WHERE users_id = ? AND datetime = ?", (user_id, date))
    
    def remove_meals(self, user_id, date, classification): 
        self.execute_delete("DELETE FROM meals WHERE users_id = ? AND datetime = ? AND classification = ?", (user_id, date, classification)) 
    
    """
    FOOD TABLE
    """
    
    def insert_foods(self, name, calories, fats, protein, carbs):
        self.execute_insert("INSERT INTO food (name, calories, fats, protein, carbs) VALUES(?, ?, ?, ?, ?)", (name, calories, fats, protein, carbs))

    def get_food_by_id(self, food_id):
        return self.execute_select("SELECT * FROM food WHERE id = ?", (food_id,))
    
    def get_food_by_name(self, food_name):
        return self.execute_select("SELECT * FROM food WHERE name = ?", (food_name,))
    
    def get_all_foods(self):
        return self.execute_select("SELECT * FROM food", ())
    
    """
    GOALS TABLE
    """
    
    def insert_goals(self, user_id, datetime, weight, calories, carbs, protein, fats):
        self.execute_insert("INSERT INTO goals (users_id, datetime, weight, calories, carbs, protein, fats) VALUES(?, ?, ?, ?, ?, ?, ?)", (user_id, datetime, weight, calories, carbs, protein, fats))

    def get_latest_goals(self, user_id):
        return self.execute_select("SELECT * FROM goals WHERE users_id = ? ORDER BY datetime DESC LIMIT 1", (user_id,))

    """
    BODY_UPDATES TABLE
    """
    
    def insert_body_updates(self, user_id, datetime, weight):
        self.execute_insert("INSERT INTO body_updates (users_id, datetime, weight) VALUES(?, ?, ?)", (user_id, datetime, weight))

    def edit_body_updates(self, user_id, datetime, weight):
        self.execute_update("UPDATE body_updates SET weight = ? WHERE users_id = ? AND datetime = ?", (weight, user_id, datetime))

    def get_body_updates(self, starting_period, user_id):
        return self.execute_select("SELECT * FROM body_updates WHERE users_id = ? AND datetime >= ? ORDER BY datetime ", (user_id, starting_period))