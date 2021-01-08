from flask import Flask, render_template, request
import wolframalpha
import pickle
import random
import webbrowser
from datetime import datetime
now = datetime.now()
now2 = now.strftime("%H:%M")

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    try:
        global f
        f=open("data\\user-data.dat","rb")
        global dict
        dict = pickle.load(f)
        return render_template("index.html",time = now2,User = dict["first-name"])
    except:
        global f1
        f1 = open("data\\user-data.dat","wb")
        global dict1
        dict1 = {}
        print("file created")
        return render_template("new-user.html")

@app.route("/success",methods = ["POST"])
def success():
    print("Inside Success")
    name_first = request.form["first-name"]
    name_last = request.form["last-name"]
    email = request.form["email-id"]
    dict1["first-name"] = name_first
    dict1["last-name"] = name_last
    dict1["email"] = email
    pickle.dump(dict1,f1)
    f1.close()
    global f
    f=open("data\\user-data.dat","rb")
    global dict
    dict = pickle.load(f)
    print("Done")
    return render_template("index.html",time = now2,User = dict["first-name"])


@app.route("/get")
def get_bot_response():
    ##functions to be defined below this line
    userText = request.args.get('msg')
    return "Desktop Assistant is under construction"

        
    

if __name__ == "__main__":
    app.run()
