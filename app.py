from flask import Flask,render_template,request
from Models import Student


app = Flask(__name__)
app.debug=True

@app.route("/")
def home():
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


app.run()