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
lesson=[]
counter = 0
# /// three slashes means relative path

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

def check_index(index):
    global used_q_num
    print('used_q_num: ', used_q_num)
    if index in used_q_num:
        return False
    else:
        return True

# funkcja sprawdza czy dany index znajduje sie na liscie uzytych pytan i odpowiedzi

def get_index(data):
    print('wywołanie get_index')
    global used_q_num
    l = len(data)-1
    if len(used_q_num) > l:
        print('ćwiczenie gotowe')
        return 0
    index = randint(0, l)
    check = check_index(index)
    if check == True:
        used_q_num.append(index)
        return index
    else:
        return get_index(data)

# powinna zwrócić index nie zadanego pytania

def get_q(index, data):
    print('inddex at get q: ', index)
    global lesson
    q_and_a =  data[index]
    for i, j in q_and_a.items():
        excercise = (i, j)
        lesson.append(excercise)
        return excercise

# funkcja zwraca pytanie i odpowiedź

def done(data):
    global used_q_num
    if len(used_q_num) >= len(data):
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
        global lesson
        global counter
        lesson = []
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
    global lesson
    global counter
    lesson = []
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
    data = get_data()
    index = get_index(data)
    current_question = ''
    
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
        question = get_q(index, data)
        if done(data) == False:
            return question[0]
        else:
            return 'gratulacje przerobiłaś wszystko na dziś'

    elif section == 'page4':
        if request.method == 'POST':
            s_l=[]
            global success
            success = False
            target = request.json['userAnswer']
            print('indexat page 4', index)
            answer =  lesson[counter][1]
            if target == answer:
                success = True
            else:
                success = False
            success=str(success)
            s_l.append(success)
            new = get_q(index, data)
            counter += 1
            s_l.append(new[0])
            if done(data) == False:
                return jsonify({'results':s_l})
        bmf = 'bmf bmf bmf bmf bmf bmf bmf bmf bmf bmf bmf '
        return bmf
    elif section == 'page3':
        rd=[]
        data = get_data()
        for i in data:
            for q,a in i.items():
                rd.append(q)
        return jsonify({'Q':rd})

