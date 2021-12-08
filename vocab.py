from flask import Flask, request, redirect, session,  render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
app.secret_key = b'gdshsgh/.,565'
db = SQLAlchemy(app)
used_q_num = []
# lista użytych indeksów
success = False
user='anonimowy'
counter = 0
# /// three slashes means relative path
data = []
index = int()


class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'name: {self.name}'

# user użytkownika

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(20), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('vocabs', lazy=True))
    def __repr__(self):
        return f' has Question: {self.question} and And Answer: {self.answer}'

# model pytań i odpowiedzi

#class Training(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    now  = datetime.datetime.now()
#    answered = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#    user = db.relationship('User', backref=db.backref('vocabs', lazy=True))
#    right = db.Column(db.Boolean, default=False, nullable=False)
#    question_id = db.Column(db.Integer, db.ForeignKey('vocab.id', nullable=False)
    #  def __repr__(self):
    #    return f'{self.answered}'

# model wykonywanych ćwiczeń

def get_user_id():
    id = 1
    if session:
        print('there is a session')
        un = session['user']
        u = User.query.filter_by(name=un).first()
        id = u.id
        print('id: ', id)
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

def get_index(data):
    print('wywołanie get_index')
    l = len(data)-1
    index = randint(0, l)
    return index

# powinna zwrócić index nie zadanego pytania

def get_q(index, data):
    print('inddex at get q: ', index)
    q_and_a =  data[index]
    for i, j in q_and_a.items():
        excercise = (i, j)
        return excercise

# funkcja zwraca pytanie i odpowiedź


def check_answer(index, data):
    print('index at check_answer: ', index)
    print('data at check_answer', data)
    target = request.json['userAnswer']
    answer_dict = data[index]
    key = ''
    for i in answer_dict.keys():
        key = i
    answer = answer_dict[key]
    print(target , ' ', answer, ' at check_answer')
    if target == answer:
        del data[index]
        print('data at check_answer after right answer: ', data)
        return True
    else:
        return False

# funkcja sprawdza czy wszystkie ćwiczenia zostały wykonanane

@app.route("/", methods=['GET', 'POST'])
def play():
    if 'user' in session:
        print(f'użytkownik zalogowany {session["user"]}')
        global user
        user = session['user']
        return render_template('spa.html', success=str(success), user=user)
    return render_template('spa.html', success=str(success), user=user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        counter = 0
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
    global counter
    counter = 0
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
    global counter
    global data
    data = get_data()
    global index
    current_question = ''
    congrats = '<h1>Gratulacje przerobiłaś wszystko na dziś</h1>'

    print('index at rsplit: ', index)

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
        if data:
            index = get_index(data)
            question = get_q(index, data)
            return question[0]
        else:
            return congrats

    elif section == 'page4':
        if request.method == 'POST':
            result = check_answer(index=index, data=data)
            if data:
                q = get_q(index, data)
                q_a = [result, q[0]]
                print('to zwraca page4: ', q_a)
                return jsonify({'results':q_a})
            else:
                return congrats
        return '<h1>coś nie tak</h1>'
    elif section == 'page3':
        rd=[]
        material = get_data()
        for i in material:
            for q,a in i.items():
                rd.append(q)
        return jsonify({'Q':rd})

