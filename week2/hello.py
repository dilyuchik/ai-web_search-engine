from flask import Flask, request

# create app object
app = Flask(__name__)

@app.route("/")
def start():
    return """<h1>Hello world.</h1>
    <img src='https://www.uni-osnabrueck.de/fileadmin/documents/public/0_startseite/start_2024/2024-12-5_foerderpreise_531px.jpg'>
    <p>OK.</p>
    <a href='/about'>About</a>"""

@app.route("/about")
def about():
    return "<p>About!</p>"