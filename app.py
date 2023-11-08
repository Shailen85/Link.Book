import os
import sqlite3 
import config

from flask import Flask, g, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, search_bar, category_list, subjects_list, searching

# Configure application
app = Flask(__name__)
app.config.from_pyfile('config.py')
#app.config['DATABASE'] = 'book.db'
app.config[' DATABASE_URL'] = 'mysql://dq18g0nck4l0xkui:pr8p7zw67k2jcr5f@jhdjjtqo9w5bzq2t.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/l724tkvf41ex5c8f'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Allows using column names for result retrieval
    return g.db

def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.before_request
def before_request():
    g.db = get_db()

@app.route("/layout", methods = ["GET", "POST"])
@login_required
def title_search():
    category = []
    subject = []
    title = []
    links = []
    description = []
    user_id = int(session["user_id"])
    # title search bar to get information of title and go to title.html to display information     
    if request.method == "POST" and request.form.get("search"):
        search = request.form.get("search")
        titles = g.db.execute("SELECT title, url_link, subject, category, description FROM content WHERE user_id=? AND title LIKE ?", (user_id, f"%{search}%")).fetchall()
        title.extend([row[0] for row in titles])
        links.extend([row[1] for row in titles])
        subject.extend([row[2] for row in titles])
        category.extend([row[3] for row in titles])
        description.extend([row[4] for row in titles])
            
        return render_template("titles.html",titles=search_bar(), title_search= search_bar(), search=search, title_name=','.join(title), link=','.join(links), subject=','.join(subject), category_name=','.join(category), d_name=','.join(description) )
    else:
       return render_template ("apology.html", message="please input title") 
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        name = request.form.get("username")
        db = get_db()
        cursor = db.cursor()
        names = db.execute("SELECT username FROM users")

        if not request.form.get("email"):
            return render_template ("apology.html", message="email required")
        if not request.form.get("username"):
            return render_template ("apology.html", message="username required")
        if not request.form.get("password"):
            return render_template ("apology.html", message="password required")
        if not request.form.get("confirmation"):
            return render_template ("apology.html", message="confirm password")
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template ("apology.html", message="password not confirmed correctly")
        for row in names:
            if row['username'] == name:
                cursor.close()
                return render_template ("apology.html", message="allready used")

        else:
            email = request.form.get("email")
            name = request.form.get("username")
            password = generate_password_hash(request.form.get("password"))

            db.execute("INSERT INTO users (username, hash, email) VALUES (?,?,?)", (name, password, email))
            db.commit()

            return redirect("/")

    return  render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db = get_db()
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template ("apology.html", message="username not entered")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template ("apology.html", message="password not entered")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",(request.form.get("username"),)).fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            # return render_template ("apology.html", message="password incorrect")
            return render_template("login.html")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    """Show page details""" 
    # get user name to say hello
    user_id = int(session["user_id"])
    dataname = g.db.execute("SELECT username FROM users WHERE id= ?", (user_id,)).fetchone()
    name = dataname["username"]
    name = name.upper()
    if request.method == "POST" and request.form.get("table_info"):
        user_id = int(session["user_id"])
        table_info = g.db.execute("SELECT category, subject, title, description, url_link FROM content WHERE user_id = ? ORDER BY category ASC", (user_id,))
        return render_template("index.html", username=name, title_search=search_bar(), table_info=table_info)
    else:
        return render_template("index.html", username=name, title_search=search_bar())

@app.route("/category", methods=["GET","POST"])
@login_required
def catogrie_list():
    """Show page details""" 
    
    # variables for category.html
    subjects = []
    subject_list = []
    titles=[]
    selected_categories = '' # used to list subjects when clicking on category
    form_edit = ''
    form_delete = ''
    form_html = ''
    edit_title = ''
    body_img = ''
    user_id = int(session["user_id"])
    

    # get list of subjects and titles when clicking on a left category 
    if request.method == "POST" and request.form.get("generate-subject") or request.form.get("search"):
        if request.form.get("generate-subject"):
            selected_categories = request.form.getlist("generate-subject")  # Get selected categories as a list
        
            try:
                # Loop through selected categories and retrieve subjects for each category
                for category in selected_categories:
                    category_data = []
                    category_data = g.db.execute("SELECT subject, title FROM content WHERE user_id=? AND category=?", (user_id, category)).fetchall()
                    subjects.extend([row[0] for row in category_data])
                    titles.extend([row[1] for row in category_data])
                # print(subjects)
                # print(titles)
            except Exception as e:
                print("Error:", str(e))

        # go to titles page when clicking on play button subject and titles list
        elif request.form.get("search"):
            search_query = request.form.get("search")
            search_results = searching(user_id, search_query)
            return render_template("titles.html", title_search=search_bar(), titles=search_bar(), search=search_query, **search_results)
        
    # edit/delete button on category details and main page to get EDIT or DELETE FORM
    elif request.method =="POST" and request.form.get("generate-delete-form") or request.form.get("option_select") or request.form.get("change") or request.form.get("change_name"):
        
        # if edit or delete button sellected generate EDIT or DELETE FORM
        if request.form.get("generate-delete-form") or request.form.get("option_select"):
            form_delete = '<form action="/category" method="post">'
            edit_title = request.form.get("generate-delete-form") or request.form.get("option_select")
            category_data = []
            category_data += g.db.execute("SELECT subject, title FROM content WHERE user_id=? AND category=?", (user_id, edit_title)).fetchall()
            subject_list.extend([row[0] for row in category_data])
            titles.extend([row[1] for row in category_data])
            
        # delete category
        elif request.form.get("delete_name"):
            db = get_db()
            user_id = int(session["user_id"])
            delete_name = request.form.get("delete_name")
            db.execute("DELETE FROM content WHERE user_id = ? and category = ?", (user_id, delete_name))
            db.commit()
            return redirect("/category")

        # edit category name
        elif request.form.get("change") or request.form.get("change_name"):
            if not request.form.get("edit_category_name"):
                return render_template ("apology.html", message="missing")
            else:
                db = get_db()
                user_id = int(session["user_id"])
                new_name = request.form.get("edit_category_name")
                new_name = new_name.upper()
                old_name = request.form.get("change_name")
                db.execute("UPDATE content SET category= ? WHERE user_id= ? AND category= ?", (new_name, user_id, old_name))
                db.commit()
                return redirect("/category")
        
    # edit/delete button on main page to get a input for category
    elif request.method =="POST" and request.form.get("generate-edit-form"):
        if request.form.get("generate-edit-form"):
            form_edit = '<form action="/category" method="post">'

    # link.book button on page to return to index page with table
    elif request.method == "GET" or request.method == "POST" and request.form.get("table_info"):
        body_img = '<form action="/category" method="post">'
        if request.method == "POST" and request.form.get("table_info"):
            user_id = int(session["user_id"])
            table_info = g.db.execute("SELECT category, subject, title, description, url_link FROM content WHERE user_id = ? ORDER BY category ASC", (user_id,))
            return render_template("index.html", title_search=search_bar(), table_info=table_info )

    # get a create form to enter a new category in database 
    elif request.method == "POST":
        if  request.form.get("generate-form"):
            form_html = '<form action="/category" method="post">'
        
        else:
            if request.method == "POST":
                db = get_db()
                user_id = int(session["user_id"])
                dataname = db.execute("SELECT username FROM users WHERE id= ?", (user_id,)).fetchone()
                name = dataname["username"]
                
                

                if not request.form.get("category"):
                    return render_template ("apology.html", message="Book Name missing")
                if not request.form.get("subject"):
                    return render_template ("apology.html", message="Chapter Name missing")
                if not request.form.get("link"):
                    return render_template ("apology.html", message="Url Link missing")
                if not request.form.get("title"):
                    return render_template ("apology.html", message="Title missing")
                
                
                else:
                    category = request.form.get("category")
                    category = category.upper()
                    subject = request.form.get("subject")
                    subject = subject.upper()
                    link = request.form.get("link")
                    description = request.form.get("description")
                    title = request.form.get("title")
                    title = title.upper()
                    title_search = g.db.execute("SELECT title FROM content WHERE title = ?",(title,)).fetchone()
                    if title_search:
                        return render_template("apology.html", message="Title already taken")


                    db.execute("INSERT INTO content (date, user_id, username, category, subject, title, description, url_link) VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?,?)", (user_id, name, category, subject, title, description, link))
                    db.commit()

                    return redirect("/category")
         
    return render_template("category.html", subjects=subjects, subject_list= subject_list, categories=category_list(), title_search= search_bar(),
                            form_delete=form_delete, form_html=form_html, forms_edit= form_edit, edit_title= edit_title, title=titles,
                              selected_categories=','.join(selected_categories), body_img= body_img, subject_option=subjects_list())

@app.route("/subject", methods=["GET", "POST"])
@login_required
def subject_list():
    """Show page details""" 
    title_list = [] 
    category_name = []
    subject=''
    links = []
    edit_subject= ''
    form_edit = ''
    form_delete = ''
    body_img = ''
    user_id = int(session["user_id"])

    # get titles and play button for subject form
    if request.method == "POST" and request.form.getlist('subjects') or request.form.get("search"):
        if request.form.getlist('subjects'):
            selected_subjects = request.form.getlist('subjects')  # Get selected subjects as a list
            try:
                title_list_data = []

                # Loop through selected categories and retrieve subjects for each category
                for subject in selected_subjects:
                    title_list_data += g.db.execute("SELECT title FROM content WHERE user_id=? AND subject=?", (user_id, subject)).fetchall()
                    title_list.extend([row[0] for row in title_list_data])
            except Exception as e:
                print("Error:", str(e))

        # go to titles page when clicking on play button subject and titles list
        elif request.form.get("search"):
            search_query = request.form.get("search")
            search_results = searching(user_id, search_query)
            return render_template("titles.html", title_search=search_bar(), titles=search_bar(), search=search_query, **search_results)
    
    # generat edit form to select subject for editing or deleting
    elif request.method =="POST" and request.form.get("generate-edit-form"):
        if request.form.get("generate-edit-form"):
            form_edit = '<form action="/subject" method="post">'

    # edit/delete button on subject details and main page to get EDIT or DELETE FORM
    elif request.method =="POST" and request.form.get("generate-delete-form") or request.form.get("option_select") or request.form.get("change") or request.form.get("change_name"):
        

        # if edit or delete button sellected generate EDIT or DELETE FORM
        if request.form.get("generate-delete-form") or request.form.get("option_select"):
            form_delete = '<form action="/subject" method="post">'
            edit_subject = request.form.get("generate-delete-form") or request.form.get("option_select")
            category_names = g.db.execute("SELECT DISTINCT category FROM content WHERE user_id=? AND subject=?", (user_id, edit_subject))
            category_name.extend([row[0] for row in category_names])
            titles_data = g.db.execute("SELECT title FROM content WHERE user_id=? AND subject=?", (user_id, edit_subject)).fetchall()
            title_list.extend([row[0] for row in titles_data])
            
        # delete category
        elif request.form.get("delete_name"):
            db = get_db()
            user_id = int(session["user_id"])
            delete_name = request.form.get("delete_name")
            db.execute("DELETE FROM content WHERE user_id = ? and subject = ?", (user_id, delete_name))
            db.commit()
            return redirect("/subject")

        # edit category name
        elif request.form.get("change") or request.form.get("change_name"):
            if not request.form.get("edit_subject_name"):
                return render_template("apology.html", message = 'mis')
            else:        
                db = get_db()
                user_id = int(session["user_id"])
                new_name = request.form.get("edit_subject_name")
                new_name = new_name.upper()
                old_name = request.form.get("change_name")
                db.execute("UPDATE content SET subject= ? WHERE user_id= ? AND subject= ?", (new_name, user_id, old_name))
                db.commit()
                return redirect("/subject")

    # generate create new form from category    
    elif request.form.get("generate-form"):
        categories_data = g.db.execute("SELECT DISTINCT category FROM content WHERE user_id= ?", (user_id,)).fetchall()
        categories = [category[0] for category in categories_data]
        form_html = '<form action="/category" method="post">'
        return render_template("category.html", form_html=form_html, categories=categories, subject_option=subjects_list())
    
    # link.book button on page to return to index page with table
    elif request.method == "GET" or request.method == "POST" and request.form.get("table_info"):
        body_img = '<form action="/category" method="post">'
        if request.method == "POST" and request.form.get("table_info"):
            user_id = int(session["user_id"])
            table_info = g.db.execute("SELECT category, subject, title, description, url_link FROM content WHERE user_id = ? ORDER BY category ASC", (user_id,))
            return render_template("index.html", title_search=search_bar(), table_info=table_info )

    return render_template("subject.html", category_name= ','.join(category_name), subjects=subjects_list(), 
                           titles_list=title_list, title_search=search_bar(), subject=subject, 
                           link=','.join(links), forms_edit= form_edit, form_delete=form_delete, 
                           edit_subject=edit_subject, body_img=body_img)

@app.route("/titles", methods=["GET", "POST"])
@login_required
def title():
    category = []
    subjects = []
    title_name = []
    links = []
    description = []
    title_id =[]
    title = ''
    form_delete = ''
    form_edit = ''
    body_img = ''
    user_id = int(session["user_id"])

    if request.method == "POST" and request.form.getlist('get_link'):
        search_query = request.form.get("get_link")
        search_results = searching(user_id, search_query)
        return render_template("titles.html", title_search=search_bar(), titles=search_bar(), search=search_query, **search_results, title_id=','.join(title_id))

    # edit/delete button on main page to get a input for category
    elif request.method =="POST" and request.form.get("generate-edit-form"):
        if request.form.get("generate-edit-form"):
            form_edit = '<form action="/titles" method="post">'
    
    # edit/delete button on subject details and main page to get EDIT or DELETE FORM
    elif request.method =="POST" and request.form.get("generate-delete-form") or request.form.get("option_select") or request.form.get("change") or request.form.get("change_name") or request.form.get("scrip_update"):
        
        # if edit or delete button sellected generate EDIT or DELETE FORM
        if request.method =="POST" and request.form.get("generate-delete-form") or request.form.get("option_select"):
            form_delete = '<form action="/titles" method="post">'
            name_title = request.form.get("generate-delete-form") or request.form.get("option_select")
            title = name_title
            titles_data = []
            titles_data += g.db.execute("SELECT category, subject, description, id FROM content WHERE user_id=? AND title=?", (user_id, name_title))
            category.extend([row[0] for row in titles_data])
            subjects.extend([row[1] for row in titles_data]) 
            description.extend([row[2] for row in titles_data])

        # delete title name            
        elif request.method =="POST" and request.form.get("delete_name"):
            db = get_db()
            user_id = int(session["user_id"])
            delete_name = request.form.get("delete_name")
            db.execute("DELETE FROM content WHERE user_id = ? and title = ?", (user_id, delete_name))
            db.commit()
            return redirect("/titles")

        # edit title or description name
        elif request.method =="POST" and request.form.get("change") or request.form.get("change_name") or request.form.get("edit_description"):
            if not request.form.get("edit_title_name"):
                if request.form.get("edit_description"):
                    db = get_db()
                    user_id = int(session["user_id"])
                    old_name = request.form.get("change_name")
                    new_description = request.form.get("new_description")
                    db.execute("UPDATE content SET description= ? WHERE user_id= ? AND title= ?", (new_description, user_id, old_name))
                    db.commit()
                else:
                    return render_template("apology.html", message = "title missing")
            else:
                db = get_db()
                user_id = int(session["user_id"])
                new_name = request.form.get("edit_title_name")
                new_name = new_name.upper()
                old_name = request.form.get("change_name")
                db.execute("UPDATE content SET title= ? WHERE user_id= ? AND title= ?", (new_name, user_id, old_name))
                db.commit()
                return redirect("/titles")

    #  generate create form category
    elif request.form.get("generate-form"):
        categories_data = g.db.execute("SELECT DISTINCT category FROM content WHERE user_id= ?", (user_id,)).fetchall()
        categories = [category[0] for category in categories_data]
        form_html = '<form action="/category" method="post">'
        return render_template("category.html", form_html=form_html, categories=categories, subject_option=subjects_list())
    
    # link.book button on page to return to index page with table
    elif request.method == "GET" or request.method == "POST" and request.form.get("table_info"):
        body_img = '<form action="/category" method="post">'
        if request.method == "POST" and request.form.get("table_info"):
            user_id = int(session["user_id"])
            table_info = g.db.execute("SELECT category, subject, title, description, url_link FROM content WHERE user_id = ? ORDER BY category ASC", (user_id,))
            return render_template("index.html", title_search=search_bar(), table_info=table_info )
            
    return render_template("titles.html", titles=search_bar(), title_name=','.join(title_name), link=','.join(links), 
                           subject=','.join(subjects), category_name=','.join(category), d_name=','.join(description), 
                            form_delete= form_delete, forms_edit= form_edit, title=title, body_img=body_img, title_id=title_id )
    
@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/apology")
def apology():
    """Show page details""" 
    return render_template ("apology.html")

if __name__ == "__main__":
    app.run(debug=False)

