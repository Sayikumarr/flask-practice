from flask import Flask,render_template,request,make_response,redirect
from Models import Student
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


app = Flask(__name__)
app.debug=True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Students_Auth.db'

app.config['SECRET_KEY'] = 'sai@123'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"ID : {self.id}, Username: {self.username}"


@app.route("/")
def home():
    # db.create_all()
    number=range(2,21,2)
    return render_template("index.html",obj=number)

@app.route("/form",methods = ['GET', 'POST'])
def form():
    db = Student()
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        data = (request.form.get("rollno"),
                request.form.get('fname'),
                request.form.get('lname'),
                request.form.get('marks'))
        db.insert(data)

        allData = db.read()
        return render_template('viewData.html',data = allData)

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("password")
        user = Students(username=username,password=generate_password_hash(pwd))
        db.session.add(user)
        db.session.commit()
        response = make_response(redirect('/'))
        response.set_cookie('token',generate_auth_token(user))
        return response
    return render_template('signup.html',type = "Sign-Up!")


@app.route("/signin",methods=['GET','POST'])
def signin():
    valid = False
    
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("password")
        user = Students.query.filter(Students.username==username).first()
        if user is not None :
            if check_password_hash(user.password,pwd):
                valid = True
                response = make_response(redirect('/'))
                response.set_cookie('token',generate_auth_token(user))
                return response
        if not valid:
            return '<h1>Invalid User or Password!</h1>'
    return render_template('signup.html',type= "Sign-In!")



def generate_auth_token(user):
    return jwt.encode({ 'id': user.id },app.config['SECRET_KEY'], algorithm='HS256')


def verify_auth_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return
    return Students.query.filter(Students.id==data['id']).one()



def main():
    app.run()

if "__main__"==__name__:
    main()