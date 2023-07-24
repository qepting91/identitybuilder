import flask
from flask import request
from mimesis.enums import Locale
from mimesis import Person, Address, Datetime, Finance, Food
from datetime import datetime
import calendar

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        locale = flask.request.form.get("locale")
        birthdate_year = flask.request.form.get("birthdate_year")
        birthdate_month = flask.request.form.get("birthdate_month")
        birthdate_day = flask.request.form.get("birthdate_day")

        # Validate the birthdate
        if not (birthdate_year and birthdate_month and birthdate_day):
            return "Year, month, and day are required.", 400
        try:
            birthdate_year = int(birthdate_year)
            birthdate_month = int(birthdate_month)
            birthdate_day = int(birthdate_day)
        except ValueError:
            return "Year, month, and day must be integers.", 400

        current_year = datetime.now().year
        if birthdate_year < 1900 or birthdate_year > current_year:
            return "Year must be between 1900 and the current year.", 400
        if birthdate_month < 1 or birthdate_month > 12:
            return "Month must be between 1 and 12.", 400
        _, days_in_month = calendar.monthrange(birthdate_year, birthdate_month)
        if birthdate_day < 1 or birthdate_day > days_in_month:
            return f"Day must be between 1 and {days_in_month} for the given month and year.", 400

        birthdate = datetime(birthdate_year, birthdate_month, birthdate_day)

        # Create providers
        providers = {
            'first_name': Person(locale).first_name,
            'last_name': Person(locale).last_name,
            'email': Person(locale).email,
            'telephone': Person(locale).telephone,
            'age': Person(locale).age,
            'address': Address(locale).address,
            'birthdate': lambda: birthdate,
            'company': Finance(locale).company,
            'company_type': Finance(locale).company_type,
            'academic_degree': Person(locale).academic_degree,
            'occupation': Person(locale).occupation,
            'dish': Food(locale).dish,
            'drink': Food(locale).drink,
            'fruit': Food(locale).fruit,
            'spices': Food(locale).spices,
            'vegetable': Food(locale).vegetable
        }

        # Generate the profile
        profile = {field: generator() for field, generator in providers.items()}

        # Render the profile page
        return flask.render_template("profile.html", profile=profile)
    else:
        locales = [locale.value for locale in Locale]
        return flask.render_template("profile_edit.html", locales=locales, current_year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)
