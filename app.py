from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datetime import datetime
app = Flask(__name__) #initialising app

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    msg = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(12),nullable=False)
    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"


@app.route('/', methods=['GET','POST']) #defining end points
def start():
    if request.method=="POST":
        title = request.form['title']
        msg = request.form['msg']
        status = "Incomplete"
        todo = Todo(title=title, msg=msg, status=status)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    #used to display template folder files
    return render_template('index.html',alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
        title = request.form['title']
        msg = request.form['msg']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.msg = msg
        todo.status = "Incomplete"
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/done/<int:sno>')
def done(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    todo.status = "Complete"
    db.session.add(todo)
    db.session.commit()
    return redirect("/")

@app.route('/search',methods=['GET','POST'])
def search():
    title = request.args.get('search_title')
    alltodo = Todo.query.filter(Todo.title.ilike('%{}%'.format(title))).all()
    return render_template('search.html',alltodo=alltodo)

@app.route('/about')
def about():
    return render_template('about.html')

#used to run app
if __name__ == "__main__":
    app.run(debug=True, port=8000)