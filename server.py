from flask_app import app
from flask_app.controllers import controller_routes, controller_users, controller_categories, controller_incomes, controller_expenses

# when making new controller import them into this file

# needs to be bottom of the file
if __name__=="__main__":
    app.run(debug=True)