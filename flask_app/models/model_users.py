from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import bcrypt, DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update_one(cls , data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def update_password(cls , data):
        query = "UPDATE users SET password = %(password)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return


    @classmethod
    def show_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            users_list = []
            for user in results:
                users_list.append(cls(user))
            return users_list
        return []


    @staticmethod
    def validator_create_user(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:            # checks first name
            is_valid = False
            flash("First Name Required", "err_user_first_name")
        elif form_data['first_name'].isalpha() == False:
            is_valid = False
            flash("Only Letters", "err_user_first_name")


        if len(form_data['last_name']) < 2:             # checks last name
            is_valid = False
            flash("Last Name Required", "err_user_last_name")
        elif form_data['last_name'].isalpha() == False:
            is_valid = False
            flash("Only Letters", "err_user_last_name")


        if len(form_data['email']) < 2:
            is_valid = False
            flash("Enter Email", "err_user_email")         # checks email

        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash("Invalid email address!", "err_user_email")

        else:
            potential_email = User.get_by_email({'email': form_data['email']})
            if potential_email != False:
                is_valid = False
                flash("Email Exists", "err_user_email")
        

        if len(form_data['password']) < 8:                  # checks password
            is_valid = False
            flash("Password required", "err_user_password")

        if len(form_data['confirm_password']) < 8:
            is_valid = False
            flash("Confirm password", "err_user_confirm_password")

        elif form_data['password'] != form_data['confirm_password']:       # compares password and confirm password
            is_valid = False
            flash("passwords do not match", "err_user_confirm_password")

        if 'not_robot' not in form_data:
            is_valid = False
            flash("Check the box", "err_user_not_robot")

        
        return is_valid



    @staticmethod
    def validator_login(form_data):
        is_valid = True

        if len(form_data['email']) < 2:
            is_valid = False

        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False

        if len(form_data['password']) < 2:
            is_valid = False
        else:
            potential_user = User.get_by_email({'email': form_data['email']})
            if not potential_user:
                is_valid = False
            elif not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                is_valid = False
            else:
                session['uuid'] = potential_user.id

        if is_valid == False:
            flash("Invalid Credentials", "err_user_password_login")

        return is_valid
