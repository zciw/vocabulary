from flask import Flask, render_template
app=Flask(__name__)

votes=0
inputs='inputs'
inp='inp'

@app.route("/")
def index():
    return render_template("side2.html", votes=votes, inputs=inputs)

@app.route("/up", methods=["POST"])
def upvote():
    global votes
    votes=votes+1
    print("votes: ", votes)
    return str(votes)

@app.route("/down", methods=["POST"])
def downvote():
    global votes
    if votes>=1:
        votes=votes-1
    return str(votes)

@app.route("/test", methods=["POST"])
def testing():
	test='new_test'
	return test

@app.route("/inputs", methods=["POST", "GET"])
def putting():
    print(f'request form: ')
    return inp
