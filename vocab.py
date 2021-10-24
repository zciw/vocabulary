from flask import Flask, request, redirect, send_from_directory
from flask import render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
db = SQLAlchemy(app)

success = False
g_key = ''
# /// three slashes means relative path

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(20), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'Question: {self.question} and And Answer: {self.answer}'

def get_data():
    all = Vocab.query.all()
    q_and_a = []
    for i in all:
        local_q = i.question
        local_a = i.answer
        q_a = {}
        q_a[local_q] = local_a
        q_and_a.append(q_a)
    return q_and_a

@app.route("/", methods=['GET', 'POST'])
def play():
    return render_template('spa.html', success=str(success))


@app.route("/<section>", methods=['GET', 'POST'])
def rsplit(section):
    data = get_data()
    key = ''
    index = len(data)-3
    question =  data[index]
    for i in question.keys():
        key = i
    if section == 'page5':
        if request.method == 'POST':
            q = request.json['question']
            a = request.json['answer']
            item = Vocab(question=q, answer=a)
            db.session.add(item)
            db.session.commit()
            return 'wtf1'
        return 'wtf2'

    elif section == 'page2':
        return key   

    elif section == 'page4':
        if request.method == 'POST':
            global success
            success = False
            target = request.json['userAnswer']
            if target == data[index][key]:
                print('success')
                success = True
            else:
                success = False
            success=str(success)
            return success
        return success
    else:
        rd=[]
        for i in data:
            for q,a in i.items():
                rd.append(q)
        print('rd: ', rd)
        return jsonify({'Q':rd})
