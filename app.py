import os
from flask import Flask, render_template, request
import wolframalpha
import pickle
import random
import webbrowser
from datetime import datetime
import yagmail
from email_validator import validate_email, EmailNotValidError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import wikipedia
import sqlite3

now = datetime.now().strftime("%H:%M")
user_commands = []
bot_response = []
app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    try:
        global f
        f=open("data\\user-data.dat","rb")
        global dict
        dict = pickle.load(f)
        return render_template("index.html",time = now,User = dict["first-name"])
        
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
    password = request.form["password"]
    dict1["first-name"] = name_first
    dict1["last-name"] = name_last
    dict1["email"] = email
    dict1["password"] = password
    pickle.dump(dict1,f1)
    f1.close()
    global f
    f=open("data\\user-data.dat","rb")
    global dict
    dict = pickle.load(f)
    print("Done")
    return render_template("index.html",time = now,User = dict["first-name"])


@app.route("/get")
def get_bot_response():
    ##functions to be defined below this line

    userText = request.args.get('msg').lower()
    lst = userText.split(" ")

    for i in lst:
        if ("mail" or "email" or "message") in userText and "@" in userText:
            for i in lst:
                if "@" in i:
                    global mail_addr
                    mail_addr=i
                    try:
                        valid = validate_email(mail_addr)
                        mail_addr = valid.email
                        bot_response.append("mail-with-id")
                        return random.choice(["Please specify the message","What is the message?","What will be the message?"])

                    except Exception as e:
                        print(e)
                        return "Looks like the provided mail id is not valid. Please check the mail id you have provided. "

        elif ("mail" or "email") in i.lower():
            bot_response.append("mail-without-id")
            return random.choice(["Please specify a mail-id","Please mention the mail-id of the recipient."])

    if bot_response!=[] and bot_response[-1]=="mail-with-id":
        mailer = yagmail.SMTP(dict["email"],dict["password"])
        try:
            mailer.send(mail_addr,"Message from "+dict["first-name"],userText)
            bot_response.clear()
            return random.choice(["Got it! The mail has been sent 👍","The message has been sent 👍","Mail send 👍"])
        except:
            return 'Oops! Looks like I\'m unable to send the mail because Google is blocking me from doing so. Please go to <a href="https://www.google.com/settings/security/lesssecureapps">this link</a> to allow me to send mails'


    elif "news" in userText:     #Data scraping from a google
        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = BeautifulSoup(xml_page, "html.parser")
        news_list = soup_page.findAll("item")
        news = "Here are some news"
        for news in news_list[:3]:
            news = news + "\n" + news.title.text
        return news
    
    elif "wikipedia" in userText:
        query = userText.replace("wikipedia", "").lstrip()
        summary = wikipedia.summary(query, sentences = 3)
        return summary

    elif "play music" in userText:
        music_directory = ""
        music_ext = ["mp3", "wav", "ogg"]
        playables = [i for i in os.listdir(music_directory) if i.split(".")[-1] in music_ext]

        if len(playables) == 0:
            return f"Found no audio file in {music_directory}. Try changing the directory or add some songs into it."
        os.startfile(random.choice(playables))

    elif "add a todo" in userText:
        todo = userText.replace("add a todo", "").lstrip()
        conn = sqlite3.connect("todos.db")
        date = datetime.now().strftime("%d/%m/%Y")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS todos (todo text, date text)")
        c.execute("INSERT INTO todos VALUES (:todo, :date)", {"todo":todo, "date":date})
        conn.commit()
        conn.close()
        return f"Todo named {todo} added successfully into the database!"
    
    elif 'delete a todo' or "complete a todo" in userText:
        todo = userText.replace("delete a todo", "").replace("complete a todo", '').lstrip()
        conn = sqlite3.connect("todos.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS todos (todo text, date text)")
        c.execute("SELECT * FROM todos WHERE todo = :todo", {"todo":todo})
        if len(c.fetchall()) == 0:
            return f"No todo named {todo} found in the database!"

        c.execute("DELETE FROM todos WHERE todo = :todo", {"todo":todo})
        conn.commit()
        conn.close()
        return f"Todo named {todo} deleted successfully from the database!"

    elif "view todos" in userText:
        conn = sqlite3.connect("todos.db")
        c = conn.cursor()
        c.execute("SELECT * FROM todos")
        data = "Here are all the todos you've added:\n"
        for i in c.fetchall():
            todo = i[0]
            date = i[1]
            data += f"{todo} - {date}\n"
        return data

if __name__ == "__main__":
    app.run()