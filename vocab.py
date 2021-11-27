from flask import Flask, request, redirect, send_from_directory, session
from flask import render_template, jsonify, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocab.db'
app.secret_key = b'gdshsgh/.,565'
db = SQLAlchemy(app)
used_q_num=[]
success = False
g_key = ''
user='anonimowy'
# /// three slashes means relative path

class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'name: {self.name}'

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(20), unique=True, nullable=False)
    answer = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('vocabs', lazy=True))
    def __repr__(self):
        return f' has Question: {self.question} and And Answer: {self.answer}'

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

data = get_data()

def check_index(index):
    global used_q_num
    if index in used_q_num:
        return False
    else:
        return True

def get_index(deta=get_data()):
    index = randint(0, len(data)-1)
    check = check_index(index)
    if check == True:
        used_q_num.append(index)
        return index
    else:
        return get_index()

q_num = get_index()

def get_q(index=q_num, data=get_data()):
    question =  data[index]
    for i in question.keys():
        return i

question = get_q()

def done():
    global used_q_num
    global data
    print('used_q_num length: ', len(used_q_num))
    if len(used_q_num) >= len(data)-20:
        return True
    else:
        return False


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
    global data
    global question
    global q_num

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
        print('done: ', done())
        if done() == False:
            return question
        else:
            return 'gratulacje przerobiłaś wszystko na dziś'

    elif section == 'page4':
        s_l = []
        if request.method == 'POST':
            global success
            success = False
            target = request.json['userAnswer']
            print('q_num and q: ', q_num, get_q(index=q_num))
            print('sys_answ: ', data[q_num][get_q(index=q_num)])
            if target == data[q_num][get_q(index=q_num)]:
                print('success')
                success = True
            else:
                success = False
            q_num = get_index()
            success=str(success)
            s_l.append(success)
            new_q = get_q(index=q_num)
            s_l.append(new_q)
            s_l.append(done())
            return jsonify({'results':s_l})
        return s_l
    elif section == 'page3':
        rd=[]
        data = get_data()
        for i in data:
            for q,a in i.items():
                rd.append(q)
        print('rd: ', rd)
        return jsonify({'Q':rd})

