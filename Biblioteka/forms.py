from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired
import json

choices_list=[]
def reload_authors():
    try:
        with open("authors.json", 'r') as f:
            authors_list = json.load(f)
    except FileNotFoundError:
        authors_list = []
    choices_list.clear()
    for author in authors_list:
        choices_list.append(f"{author.get('first_name')} {author.get('last_name')}")
reload_authors()


class BookForm(FlaskForm):
    title=StringField("Tytuł", validators=[DataRequired()])
    author=SelectField("Autor",choices = choices_list, validators=[DataRequired()])
    read=BooleanField("Czy przeczytana")
    length=IntegerField("Ilość stron", validators=[DataRequired()])

class AuthorForm(FlaskForm):
    first_name=StringField("Imie", validators=[DataRequired()])
    last_name=StringField('Nazwisko', validators=[DataRequired()])

