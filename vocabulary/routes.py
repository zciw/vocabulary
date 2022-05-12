from flask import request, redirect, session,  render_template, jsonify, url_for
from random import randint
from datetime import datetime
import json
from vocabulary import app, db
from vocabulary.models import User, Vocab, Lesson
filename = 'vocab.txt'


def get_user_id():
    id = 1
    if session:
        try:
            print('there is a session')
            un = session['user']
            u = User.query.filter_by(name=un).first()
            id = u.id
            return id
        except AttributeError:
            print('exception work what now and fucktion return id no 1')
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
        login_counter =  User.query.filter_by(name=user).first().logged_counter
        print('login counter: ',login_counter)
        return jsonify({'success' :'False', 'user':user, 'login_counter':login_counter})
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    loged = False
    if request.method == 'POST':
        users = User.query.all()
        print('users list from login funcktion: ', users)
        try_user = request.form['user']
        for i in users:
            if str(i) == try_user:
                loged = True
                session['user'] = try_user
                dbu = User.query.filter_by(name=try_user).first()
                dbu.logged_counter +=1
                db.session.commit()
            else:
                print(f'user: {i}, try_user: {try_user}') 
                print('nie zalogowany')
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

    if section == 'qa':
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

    elif section == 'learn':
        data = get_data()
        if data:
            lesson = Lesson(data)
            excercise = lesson.make_excercise()
            question = excercise[1]
            return question
        else:
            return 'no data'

    elif section == 'submit_answer':
        if request.method == 'POST':
            target = request.json['userAnswer']
            result = lesson.check_excercise(target ,excercise[2],excercise[0]) 
            excercise = lesson.make_excercise()
            question = excercise[1]
            with open(filename, 'a') as f:
                f.write(f'{result}\n')
            q_a = [result, question]
            return({'results':q_a})
        return jsonify({'message':'coś nie tak'})

    elif section == 'all_questions':
        rd=[]
        material = get_data()
        for i in material:
            for q,a in i.items():
                rd.append(q)
        return jsonify({'Q':rd})

    elif section == 'rank':
        l=[]
        users = User.query.all()
        for user in users:
            item = str(user)
            l.append(item)
        return jsonify({'users':l})

