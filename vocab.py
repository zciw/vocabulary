from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
db = SQLAlchemy(app)

# /// three slashes means relative path

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(20), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'Question: {self.question} and And Answer: {self.answer}'

@app.route("/")
def run():
    return render_template("main.html",name="'so faar nothing'")

@app.route("/<section>", methods=['GET', 'POST'])
def split(section):
    
    name=''
    all = Vocab.query.all()
    q_a = {}
    q_and_a = []
    for i in all:
        local_q = i.question
        local_a = i.answer
        q_a[local_q] = local_a
        q_and_a.append(q_a)
    name=q_a
    # if request.method == 'POST':
    #     q = request.form['question']
    #     a = request.form['answer']
    #     item = Vocab(question=q, answer=a)
    #     db.session.add(item)
    #     db.session.commit()
    data=['a', 'name', 'c']
    num=int(section)
    if 1 <= num <=3:
        return data[section-1]
