from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE


class Expense:
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.description = data['description']
        self.cost = data['cost']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.category_id = data['category_id']


    @classmethod
    def create_expense(cls, data):
        query = "INSERT INTO expenses (date, description, cost, category_id) VALUES (%(date)s, %(description)s, %(cost)s, %(category_id)s);"
        expense_id = connectToMySQL(DATABASE).query_db(query, data)
        return expense_id

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM expenses WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_all_category_expenses(cls, data):
        query = "SELECT * FROM expenses WHERE category_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            expense_list = []
            for expense in results:
                expense_list.append(cls(expense))
            return expense_list
        return []

    @classmethod
    def update_one(cls , data):
        query = "UPDATE expenses SET date = %(date)s, description = %(description)s, cost = %(cost)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM expenses WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return
    
    @staticmethod
    def validator_create_expense(form_data):

        is_valid = True

        if len(form_data['date']) != 10:
            is_valid = False
            flash("Use valid date", "err_expense_date")

        if len(form_data['description']) < 2:
            is_valid = False
            flash("At least 2 character description", "err_expense_description")

        if len(form_data['cost']) < 1:
            is_valid = False
            flash("Enter a Value", "err_expense_cost")
        elif int(form_data['cost']) < 0:
            is_valid = False
            flash("Enter a valid number", "err_expense_cost")

        if 'category_id' in form_data:
            if len(form_data['category_id']) < 1:
                is_valid = False
                flash("Create a Category", "err_expense_category")

        return is_valid

