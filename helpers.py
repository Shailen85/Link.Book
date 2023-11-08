from flask import redirect, render_template, session, request, g, Flask
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'key111213'
#app.config["DEBUG"] = True
app.config['DATABASE'] = 'book.db'

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Allows using column names for result retrieval
    return g.db


def search_bar():
    user_id = int(session["user_id"])
    titles_data = g.db.execute("SELECT title FROM content WHERE user_id= ?", (user_id,)).fetchall()
    title_search = [row[0] for row in titles_data]
    return title_search

def category_list():
    user_id = int(session["user_id"])
    category_data = g.db.execute("SELECT DISTINCT category FROM content WHERE user_id= ?", (user_id,)).fetchall()
    category_titles = [row[0] for row in category_data]
    return category_titles

def subjects_list():
    user_id = int(session["user_id"])
    subject_data = g.db.execute("SELECT DISTINCT subject FROM content WHERE user_id= ?", (user_id,)).fetchall()
    subjects = [row[0] for row in subject_data]
    return subjects

def searching(user_id, search_query):
    search = []
    category = []
    subject = []
    title = []
    link = []
    description = []

    search_data = g.db.execute("SELECT title, url_link, subject, category, description FROM content WHERE user_id=? AND title LIKE ?", (user_id, f"%{search_query}%")).fetchall()
    
    title.extend([row[0] for row in search_data])
    link.extend([row[1] for row in search_data])
    subject.extend([row[2] for row in search_data])
    category.extend([row[3] for row in search_data])
    description.extend([row[4] for row in search_data])

    return {
        "title_name": ','.join(title),
        "link": ','.join(link),
        "subject": ','.join(subject),
        "category_name": ','.join(category),
        "d_name": ','.join(description)
    }