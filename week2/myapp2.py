from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/reversed")
def reversed():
    rev = request.args['rev'][::-1] # process argument, such that it is displayed in reversed order
                                    # args is a dictionary organized by names given to form elements
    return render_template('reversed.html', rev=rev) # can also give list of search hits e.g., and loop through them

