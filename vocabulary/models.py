from random import randint
from vocabulary import db


print(db)


class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'

# user użytkownika

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(30), unique=True, nullable=False)
    answer = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('vocabs', lazy=True))
    def __repr__(self):
        return f' has Question: {self.question} and And Answer: {self.answer}'

class Lesson():

    def __init__(self, q_and_a):
        self.q_and_a = q_and_a

    def make_excercise(self):
        print('wywołanie make_excercise ')
        if self.q_and_a:
            end = len(self.q_and_a)-1
            index = randint(0, end)
            question = ''
            data =  self.q_and_a[index]
            for i in data.keys():
                question = i
            answer = data[question]
            excercise = [index, question, answer]
            return excercise
        end = ['end','', '']
        return end

    def check_excercise(self, user_answer, answer, index):
        if user_answer == answer:
            del self.q_and_a[index]
            if self.q_and_a:
                return True
            else:
                print('fertig')
                return 'fertig'
        else:
            return False

    

