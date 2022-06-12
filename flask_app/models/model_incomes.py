from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE


class Income:
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.description = data['description']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create_income(cls, data):
        query = "INSERT INTO incomes (date, description, amount, user_id) VALUES (%(date)s, %(description)s, %(amount)s, %(user_id)s);"
        income_id = connectToMySQL(DATABASE).query_db(query, data)
        return income_id

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM incomes WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_all_users_incomes(cls, data):
        query = "SELECT * FROM incomes WHERE user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            income_list = []
            for income in results:
                income_list.append(cls(income))
            return income_list
        return []

    @classmethod
    def update_one(cls , data):
        query = "UPDATE incomes SET date = %(date)s, description = %(description)s, amount = %(amount)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return


    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM incomes WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @staticmethod
    def validator_create_income(form_data): 
        is_valid = True

        if len(form_data['date']) != 10:
            is_valid = False
            flash("Use valid date", "err_income_date")

        if len(form_data['description']) < 2:
            is_valid = False
            flash("At least 2 character description", "err_income_description")

        if len(form_data['amount']) < 1:
            is_valid = False
            flash("Enter a Value", "err_income_amount")
        elif int(form_data['amount']) < 0:
            is_valid = False
            flash("Enter a valid number", "err_income_amount")

        return is_valid

