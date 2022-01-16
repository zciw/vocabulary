from flask import Flask, request, redirect, session,  render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
import json
from lesson import Lesson
filename = 'vocab.txt'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
app.secret_key = b'gdshsgh/.,565'
db = SQLAlchemy(app)
user='anonimowy'
# /// three slashes means relative path

class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'name: {self.name}'

# user użytkownika

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(30), unique=True, nullable=False)
    answer = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('vocabs', lazy=True))
    def __repr__(self):
        return f' has Question: {self.question} and And Answer: {self.answer}'

def get_user_id():
    id = 1
    if session:
        print('there is a session')
        un = session['user']
        u = User.query.filter_by(name=un).first()
        id = u.id
        return id
    return id

# funkcja zwraca primary_key aktualnie zalogowanego użytkownika lub jeżeli nikt nie jest zalogowany zwarca pk admina

def get_data():
    all = Vocab.query.filter_by(user_id=get_user_id()).all()
    print('len of all ', len(all))
    q_and_a = []
    for i in all:
        local_q = i.question
        local_a = i.answer
        q_a = {}
        q_a[local_q] = local_a
        q_and_a.append(q_a)
    return q_and_a

# funkcja zwraca liste pytań i odpowiedzi  aktualnie zalogowanego użytkownika lub admina

data = None
lesson = None
excercise = None

@app.route("/", methods=['GET', 'POST'])
def play():
    if 'user' in session:
        print(f'użytkownik zalogowany {session["user"]}')
        global user
        user = session['user']
        return render_template('spa.html', success='False', user=user)
    return render_template('spa.html', success='False', user=user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        print(session)
        return redirect(url_for('play'))
    return '''
        <form method="post">
            <p><input type=text name=user>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route("/logout")
def logout():
    session.pop('user', None)
    session['user'] = 'anonimowy'
    print(session)
    return redirect(url_for('play'))

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    session.pop('user', None)
    if request.method == 'POST':
        u = request.form['user']
        print('new user', user)
        item=User(name=u)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('play'))
    return '''
        <form method="post">
            <p><label>Podaj Twoje imie</label></P>
            <p><input type=text name=user>
            <p><input type=submit value='Zatwierdż'>
        </form>
    '''

@app.route("/<section>", methods=['GET', 'POST'])
def rsplit(section):
    
    global q_num
    global lesson
    global excercise
    global data
    current_question = ''
    congrats = '<h1>Gratulacje przerobiłaś wszystko na dziś</h1>'

    if section == 'page5':
        if request.method == 'POST':
            q = request.json['question']
            a = request.json['answer']
            u=session['user']
            print(u)
            dbu = User.query.filter_by(name=u).first()
            item = Vocab(question=q, answer=a, user_id=dbu.id)
            db.session.add(item)
            db.session.commit()
            return 'wtf1'
        return 'wtf2'

    elif section == 'page2':
        data = get_data()
        lesson = Lesson(data)
        excercise = lesson.make_excercise()
        question = excercise[1]
        return question

    elif section == 'page4':
        if request.method == 'POST':
            target = request.json['userAnswer']
            result = lesson.check_excercise(target ,excercise[2],excercise[0]) 
            excercise = lesson.make_excercise()
            question = excercise[1]
            with open(filename, 'a') as f:
                f.write(f'{result}\n')
            q_a = [result, question]
            return({'results':q_a})
        return '<h1>coś nie tak</h1>'

    elif section == 'page3':
        rd=[]
        material = get_data()
        for i in material:
            for q,a in i.items():
                rd.append(q)
        return jsonify({'Q':rd})

    elif section == 'page8':
        l=[]
        users = User.query.all()
        for user in users:
            item = str(user)
            l.append(item[6:])
        print(l)
        return jsonify({'users':l})

