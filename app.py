from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ninjatodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if(not(title and title.strip()) or not(desc and desc.strip())):
            return render_template('error.html')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method =='POST':
        title = request.form['title']
        desc = request.form['desc']
        if(not(title and title.strip()) or not(desc and desc.strip())):
            return render_template('error.html')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit() 
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)