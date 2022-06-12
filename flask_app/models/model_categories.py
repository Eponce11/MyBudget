from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE


class Category:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.expected_total = data['expected_total']
        self.total = data['total']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    

    @classmethod
    def create_category(cls, data):
        query = "INSERT INTO categories (name, description, expected_total, total, user_id) VALUES (%(name)s, %(description)s, %(expected_total)s, '0', %(user_id)s);"
        category_id = connectToMySQL(DATABASE).query_db(query, data)
        return category_id

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM categories WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_all_users_categories(cls, data):
        query = "SELECT * FROM categories WHERE user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            category_list = []
            for category in results:
                category_list.append(cls(category))
            return category_list
        return []

    @classmethod
    def update_one(cls , data):
        query = "UPDATE categories SET name = %(name)s, description = %(description)s, expected_total = %(expected_total)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return
    
    @classmethod
    def update_one_total(cls , data):
        query = "UPDATE categories SET total = %(total)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM categories WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return
    

    @staticmethod
    def validator_create_category(form_data):

        is_valid = True

        if len(form_data['name']) < 2:
            is_valid = False
            flash("At least 2 character name", "err_category_name")

        if len(form_data['description']) < 2:
            is_valid = False
            flash("At least 2 character description", "err_category_description")

        if len(form_data['expected_total']) < 1:
            is_valid = False
            flash("Enter a Value", "err_category_expected_total")
        elif int(form_data['expected_total']) < 0:
            is_valid = False
            flash("Enter a valid number", "err_category_expected_total")


        return is_valid


