from flask import Flask, render_template, request
import wolframalpha

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    #functions to be defined below this line
    userText = request.args.get('msg')
    return "Desktop Assistant is under development. Please try again later"
    

if __name__ == "__main__":
    app.run()
