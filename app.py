from flask import Flask, render_template, request
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_place", methods=["GET","POST"])
def add_one_place():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into place (name) values (:name)",request.form)
        user = query_db('select * from place')
        return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")
    user = query_db('select * from place')
    one_user = query_db("select * from place limit 1", one=True)
    return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")

@app.route("/add_one_photo", methods=["GET","POST"])
def add_one_photo():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into photo (place_id,title,pic) values (:place_id,:title,:pic)",request.form)
        user = query_db('select * from photo')
        return render_template("photoform.html", photos=user, one_user=one_user, the_title="add new photo")
    user = query_db('select * from photo')
    one_user = query_db("select * from photo limit 1", one=True)
    return render_template("photoform.html", photos=user, one_user=one_user, the_title="add new photo")

@app.route("/add_one_article", methods=["GET","POST"])
def add_one_article():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into article (place_id,month,year,content) values (:place_id,:month,:year,:content)",request.form)
        user = query_db('select * from article')
        return render_template("articleform.html", articles=user, one_user=one_user, the_title="add new article")
    user = query_db('select * from article')
    one_user = query_db("select * from article limit 1", one=True)
    return render_template("articleform.html", articles=user, one_user=one_user, the_title="add new article")

