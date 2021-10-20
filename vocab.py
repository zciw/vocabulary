from flask import Flask, request, redirect, send_from_directory
from flask import render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
db = SQLAlchemy(app)

success = False

# /// three slashes means relative path

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(20), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'Question: {self.question} and And Answer: {self.answer}'

def get_data():
    all = Vocab.query.all()
    print('all', all)
    q_and_a = []
    for i in all:
        local_q = i.question
        local_a = i.answer
        q_a = {}
        q_a[local_q] = local_a
        q_and_a.append(q_a)
    print('dane z funkcji get_data', q_and_a)    
    return q_and_a

@app.route("/", methods=['GET', 'POST'])
def play():
    return render_template('spa.html', success=str(success))


@app.route("/<section>", methods=['GET', 'POST'])
def rsplit(section):
    data = get_data()
    index = len(data)-1
    if section == 'page5':
        if request.method == 'POST':
            print('page5 request: ',request.json)
            q = request.json['question']
            a = request.json['answer']
            item = Vocab(question=q, answer=a)
            db.session.add(item)
            db.session.commit()
            return 'wtf1'
        return 'wtf2'

    elif section == 'page2':
        print('data', data)
        print('data index', data[index])
        print('index', index)
        return data[index]
    elif section == 'page4':
        if request.method == 'POST':
            global success
            success = False
            print(request.json)
            target = request.json['userAnswer']
            print(f'target is {target} and index is {index}')
            if target == data[index][q_to_show[index]]:
                print('success')
                success = True
            else:
                print('fucked')
                success = False
            success=str(success)
            return success
        return success
    else:
        return jsonify(data)
