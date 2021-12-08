from random import randint
class Lesson():

    def __init__(self, q_and_a):
        self.q_and_a = q_and_a

    def make_excercise(self):
        end = len(self.q_and_a)-1
        index = randint(0, end)
        question = ''
        data =  self.q_and_a[index]
        for i in data.keys():
            question = i
        answer = data[question]
        excercise = [index, question, answer]
        return excercise

    def check_excercise(self, user_answer, answer, index):
        if user_answer == answer:
            del self.q_and_a[index]
            print(self.q_and_a)
            return True
        else:
            print('false')
            return False

    


data = [{'front': 'css'}, {'back': 'flask'}, {'mobile': 'ios'}, {'sport': 'basket'}, {'nowsze': 'newer'}, {'early': 'morning'}]


l = Lesson(data)
excercise = l.make_excercise()
l.check_excercise('flask', excercise[2], excercise[0])
