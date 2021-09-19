from flask import Flask, request, redirect, send_from_directory
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
    q_and_a.append(local_q)

@app.route("/", methods=['GET', 'POST'])
def play():
    global q_a
    if request.method == 'POST':
        success = False
        if 'userQuestion' in request.form:
            target = request.form['userQuestion']
            print(f'target is {target}')
            if target == q_a[q_and_a[0]]:
                print('success')
                success = True
            else:
                print('fucked')
                success = False
          #  return str(success)
        else:
            q = request.form['question']
            a = request.form['answer']
            item = Vocab(question=q, answer=a)
            db.session.add(item)
            db.session.commit()
            for i in all:
                local_q = i.question
                local_a = i.answer
                q_a[local_q] = local_a
    return render_template("spa.html")

@app.route("/<section>", methods=['GET', 'POST'])
def rsplit(section):
    l=['bad','bad mother','bad mother fucker']
    all_qa = Vocab.query.all()
    q_to_show = []
    for i in all_qa:
        q=i.question
        q_to_show.append(q)
    if section == 'page1':
        return l[0]
    elif section == 'page2':
        return q_to_show[0]
    elif section == 'page4':
        print('page4')
        return 'page4'
    else:
        return jsonify(q_to_show)


# @app.route("/play_two")
# def play_two():
#    return render_template('play_two.html', n=request.args.get('n', 'bmf'))

# @app.route("/", methods=['GET', 'POST'])
# def run():
#     if request.method == 'POST':
#         q = request.form['question']
#         a = request.form['answer']
#         item = Vocab(question=q, answer=a)
#         db.session.add(item)
#         db.session.commit()
#         all = Vocab.query.all()
#         global q_a
#         for i in all:
#             local_q = i.question
#             local_a = i.answer
#             q_a[local_q] = local_a
#     return render_template("main.html")    

# @app.route("/<section>", methods=['GET', 'POST'])
# def split(section):
#     if section == 2:
#         user_question=list(q_a.keys())[0]
#         return make_response(jsonify({'user_question':user_question}))
#     elif section == 3:
#         return make_response(jsonify(q_a))
        
