from flask import Flask, request
from flask import render_template, jsonify, make_response
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

all = Vocab.query.all()
q_a = {}
q_and_a = []
for i in all:
    local_q = i.question
    local_a = i.answer
    q_a[local_q] = local_a
    q_and_a.append(q_a)


@app.route("/", methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        q = request.form['question']
        a = request.form['answer']
        item = Vocab(question=q, answer=a)
        db.session.add(item)
        db.session.commit()
        all = Vocab.query.all()
        global q_a
        for i in all:
            local_q = i.question
            local_a = i.answer
            q_a[local_q] = local_a
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route("/<int:section>", methods=['GET', 'POST'])
def split(section):
    return make_response(jsonify(q_a))