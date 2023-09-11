from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    stu_class = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__ (self) -> str:
        return f"{self.id}"
    

   

    
@app.route("/", methods=['GET','POST'])
def jsk():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        father_name = request.form['father_name']
        mobile = request.form['mobile']
        stu_class = request.form['stu_class']
        student = Student( first_name = first_name , last_name = last_name, father_name = father_name, mobile = mobile, stu_class =stu_class )
        db.session.add(student)
        db.session.commit()
    allStudent = Student.query.all()
    return render_template('index.html', allStudent=allStudent)
@app.route("/delete/<int:id>")
def delete(id):
    allStudent = Student.query.filter_by(id=id).first()
    db.session.delete(allStudent)
    db.session.commit()
    return redirect("/")
    

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        father_name = request.form['father_name']
        mobile = request.form['mobile']
        stu_class = request.form['stu_class']
        student = Student.query.filter_by(id=id).first()   
        student.first_name = first_name
        student.last_name = last_name
        student.father_name = father_name
        student.mobile = mobile
        student.stu_class = stu_class

        db.session.add(student)
        db.session.commit()
        # flash('Update successfully')        
        return redirect("/")
    student = Student.query.filter_by(id=id).first()
    return render_template('update.html', student=student)

@app.route("/add_student")
def add_student():
    return render_template('add_student.html')

if __name__ == "__main__":
    app.run(debug=True, port=7000)
