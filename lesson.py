from random import randint
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

    

