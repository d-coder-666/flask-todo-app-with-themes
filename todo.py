from flask import Flask,redirect,render_template,request,url_for,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
current_path=os.getcwd()
#IF You use Windows uncomment theese and delete 15-th line
"""
path_for_db=""
for i in current_path:
    if i=='\\':
        i="/"
    path_for_db+=i
path_for_db="sqlite:////"+path_for_db[3:]+"/todo.db"
"""
path_for_db="sqlite:////"+current_path+"/todo.db"
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=path_for_db
db=SQLAlchemy(app)
app.secret_key="todo"
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/theme-dark")
def dark():
    todos=Todo.query.all()
    theme="dark"
    table_theme="table-dark"
    dark_button="light"
    light_button="light"
    session["theme"]=theme
    return render_template("app.html",theme=theme,dark_button=dark_button,light_button=light_button,todos=todos,table_theme=table_theme)
@app.route("/theme-light")
def light():
        theme="light"
        table_theme=""
        todos=Todo.query.all()
        dark_button="secondery"
        light_button="dark"
        session["theme"]=theme
        return render_template("app.html",theme=theme,dark_button=dark_button,light_button=light_button,todos=todos,table_theme=table_theme)
@app.route("/add",methods=["POST"])
def add():
    title=request.form.get("title")
    newTodo=Todo(title=title,status=False,date=datetime.ctime(datetime.now()))
    db.session.add(newTodo)
    db.session.commit()
    if session["theme"]=="dark":
        return redirect(url_for("dark"))
    else:
        return redirect(url_for("light"))

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    status=db.Column(db.Boolean)
    date=db.Column(db.Integer,nullable=False,default=(datetime.ctime(datetime.now())))
@app.route("/update/<string:id>")
def update(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.status=not todo.status
    db.session.commit()
    if session["theme"]=="dark":
        return redirect(url_for("dark"))
    else:
        return redirect(url_for("light"))
@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    if session["theme"]=="dark":
        return redirect(url_for("dark"))
    else:
        return redirect(url_for("light"))
if __name__=="__main__":
    db.create_all()
    app.run(debug=False)
