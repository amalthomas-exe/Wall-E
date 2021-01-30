import time
start = time.time()
import cryptocode
import multiprocessing
from flask import Flask, render_template,request,url_for
from gevent.pywsgi import WSGIServer
import webview
import pickle
import random
from datetime import datetime
import sqlite3
import os
from multiprocessing import Process
import urllib.request
key = "nhdjhvfjnvhfjdfnvhfjdfnhfjdnhfjdmnhfdjdfhjdkfj"
now = datetime.now().strftime("%H:%M")
bot_response = []

greetings = ["hey","hi","hello","welcome","yo"]
affirm = ["sure","yes","yup","y","why not","of cource"]
confirm = ["you got it","sure","as you wish"]
reject = ["I'm sorry I cannot do that"]
thanks = ["thanks","thank","thnx"]
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_folder = 'static'
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)
        

def add_reminder(content:str, time:str):
        """
        Adds a reminder.
        """
        conn = sqlite3.connect("data\\misc\\reminders.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS reminders (content text, time text)")
        c.execute("INSERT INTO reminders VALUES (:content, :time)", {"content":content, "time":time})
        conn.commit()
        conn.close()


def check_reminder():
    """
    Checks for reminders.
    """
    while True:   
        conn = sqlite3.connect("data\\misc\\reminders.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS reminders (content text, time text)")
        c.execute("SELECT * FROM reminders")

        now = datetime.now().strftime("%d-%m-%y %H:%M")
        for i in c.fetchall():
            if i[1] == now:
                print("reminder up")
                c.execute("DELETE FROM reminders WHERE time = :time", {"time":now})
                conn.commit()
                conn.close()
                from plyer import notification
                notification.notify(title="Reminder from Wall-E",message=f"You asked me to remind you to `{i[0]}` now.",app_name="Wall-E",app_icon="icon.ico",timeout = 15)


def check_for_connection():
    try:
        urllib.request.urlopen("https://www.google.com") 
        return True
    except:
        return False

if check_for_connection():
    @app.route("/")
    def home():
        try:
            global f
            f=open("data\\user\\user-data.dat","rb")
            global dict2
            dict2 = pickle.load(f)
            return render_template("index.html",time = now,User = cryptocode.decrypt(dict2["first-name"],key))
            
        except:
            global f1
            f1 = open("data\\user\\user-data.dat","wb")
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
        if password=="":
            dict1["first-name"] = cryptocode.encrypt(name_first,key)
            dict1["last-name"] = cryptocode.encrypt(name_last,key)
            dict1["email"] = cryptocode.encrypt("bot.walle1@gmail.com",key)
            dict1["password"] = cryptocode.encrypt("walle1234",key)
            pickle.dump(dict1,f1)
        else:
            dict1["first-name"] = cryptocode.encrypt(name_first,key)
            dict1["last-name"] = cryptocode.encrypt(name_last,key)
            dict1["email"] = cryptocode.encrypt(email,key)
            dict1["password"] =cryptocode.encrypt(password,key)
            pickle.dump(dict1,f1)
        f1.close()
        global f
        f=open("data\\user\\user-data.dat","rb")
        global dict2
        dict2 = pickle.load(f)
        print("Done")
        
        return render_template("index.html",time = now,User = cryptocode.decrypt(dict2["first-name"],key))


    @app.route("/get")
    def get_bot_response():
        ##functions to be defined below this line
        userText = request.args.get('msg').lower()
        print(userText)
        lst = userText.split(" ")
        print(lst)
        for i in lst:
            if i.lower() in greetings and len(lst)<3:
                lst.clear()
                return f"{random.choice(['hi','Hey','Hello','Welcome','Yo'])} {cryptocode.decrypt(dict2['first-name'],key)}"
            if i.lower() in thanks:
                lst.clear()
                return random.choice(["You're Welcome 😊","Oh! that's my job 😊"])
            
            elif ("mail" or "email" or "message") in userText and "@" in userText:
                for i in lst:
                    if "@" in i:
                        global mail_addr
                        mail_addr=i
                        try:
                            from email_validator import validate_email, EmailNotValidError
                            valid = validate_email(mail_addr)
                            mail_addr = valid.email
                            bot_response.append("mail-with-id")
                            lst.clear()
                            return random.choice(["Please specify the message","What is the message?","What will be the message?"])

                        except Exception:
                            lst.clear()
                            return "Looks like the provided mail id is not valid. Please check the mail id you have provided. "

            elif ("mail" or "email" or "message") in i.lower():
                bot_response.append("mail-without-id")
                lst.clear()
                return random.choice(["Please specify a mail-id","Please mention the mail-id of the recipient."])

        if bot_response!=[] and bot_response[-1]=="mail-with-id":
            import yagmail
            mailer = yagmail.SMTP(cryptocode.decrypt(dict2["email"],key),cryptocode.decrypt(dict2["password"],key))
            try:
                mailer.send(mail_addr,"Message from "+cryptocode.decrypt(dict2["first-name"],key),userText)
                bot_response.clear()
                lst.clear()
                return random.choice(["Got it! The mail has been sent 👍","The message has been sent 👍","Mail sent 👍"])
            except:
                lst.clear()
                return 'Oops! Looks like I\'m unable to send the mail because Google is blocking me from doing so. Please go to <a href="https://www.google.com/settings/security/lesssecureapps">this link</a> to allow me to send mails'
        
        elif "who" and "are" in lst or "what" and "name" and "your" in lst:
            bot_response.append(userText)
            lst.clear()
            return random.choice(["My name is wall-e","My developers named me wall-e","you can call me wall-e"])

        elif ("open" and "google") in userText:
            import webbrowser
            bot_response.append(userText)
            webbrowser.get().open("https://www.google.com",new=2)
            lst.clear()
            return "Opening Google 👍"

        elif ("open" and "discord") in lst:
            import webbrowser
            bot_response.append(userText)
            webbrowser.get().open("https://discord.com/channels/@me")
            lst.clear()
            return "Opening Discord 🎮"
        
        elif ("how are you" or "how do you do") in userText:
            lst.clear()
            return random.choice(["I'm good! Thanks for asking","I'm doing great","I'm fine"])

        elif "news" in userText:
            from bs4 import BeautifulSoup
            from urllib.request import urlopen
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = BeautifulSoup(xml_page, "html.parser")
            news_list = soup_page.findAll("item")
            news_t = "Here are some news"
            for news in news_list[0:3]:
                news_final = "<u>"+news_t + "</u><br>" + news.title.text
            lst.clear()
            return news_final
        
        elif "wikipedia" in lst:
            import wikipedia
            query = userText.replace("wikipedia", "").lstrip()
            summary = wikipedia.summary(query, sentences = 3)
            lst.clear()
            return "According to Wikipedia <br> "+summary

        elif "play music" in userText:
            import os
            music_directory = os.path.join(os.path.expanduser("~"), "Music")
            music_ext = ["mp3", "wav", "ogg"]
            playables = [i for i in os.listdir(music_directory) if i.split(".")[-1] in music_ext]

            if len(playables) == 0:
                return f"Found no audio file in {music_directory}. Try adding some songs into the music directory."

            lst.clear()
            song = random.choice(playables)
            os.startfile(os.path.join(music_directory, song))
            return f"Sure, playing {song}."

        elif "add a todo" in userText:
            todo = userText.replace("add a todo", "").lstrip()
            conn = sqlite3.connect("data\\misc\\todos.db")
            date = datetime.now().strftime("%d/%m/%Y")
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS todos (todo text, date text)")
            c.execute("INSERT INTO todos VALUES (:todo, :date)", {"todo":todo, "date":date})
            conn.commit()
            conn.close()
            lst.clear()
            return f"Todo named {todo} added successfully into the database!"
        
        elif ('delete a todo' or "complete a todo") in userText:
            todo = userText.replace("delete a todo", "").replace("complete a todo", '').lstrip()
            conn = sqlite3.connect("data\\misc\\todos.db")
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS todos (todo text, date text)")
            c.execute("SELECT * FROM todos WHERE todo = :todo", {"todo":todo})
            if len(c.fetchall()) == 0:
                lst.clear()
                return f"No todo named {todo} found in the database!"
            else:
                c.execute("DELETE FROM todos WHERE todo = :todo", {"todo":todo})
                conn.commit()
                conn.close()
                lst.clear()
                return f"Todo named {todo} deleted successfully from the database!"

        elif "view todos" in userText:
            conn = sqlite3.connect("data\\misc\\todos.db")
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS todos (todo text, date text)")
            c.execute("SELECT * FROM todos")
            data = "Here are all the todos you've added:<br>"
            for i in c.fetchall():
                todo = i[0]
                date = i[1]
                data += f"{todo} - {date}<br>"
            lst.clear()
            return data
        
        elif "youtube" in lst:
            if "search" or "play" in lst:
                import requests
                query = userText.replace("youtube", "").lstrip()
                url = 'https://www.youtube.com/results?q=' + query
                count = 0
                cont = requests.get(url)
                data = str(cont.content)
                lst = data.split('"')
                for i in lst:
                    count+=1
                    if i == 'WEB_PAGE_TYPE_WATCH':
                        break
                if lst[count-5] == "/results":
                    return "No video found."
                else:
                    vid_id_lst = lst[count-5].split("/watch?v=")
                    vid = "https://www.youtube.com/embed/"+vid_id_lst[-1]
                    return f'Sure! here you go 👍<br><iframe src={vid} title="Video" width="420" height="300"></iframe>'
            else:
                import webbrowser
                bot_response.append(userText)
                webbrowser.get().open("https://www.youtube.com",new = 2)
                lst.clear()
                return "opening youtube 📺"

        elif "joke" in userText:
            import pyjokes
            return pyjokes.get_joke()
        
        elif any(cond in userText for cond in ["facts", "fact","intresting thing","surprise me"]):
            import requests
            from bs4 import BeautifulSoup
            data = requests.get("https://www.generatormix.com/random-facts-generator").content
            soup = BeautifulSoup(data)
            fact = soup.find("blockquote",attrs = {'class':"text-left"})
            return "<p>Here's a fun fact</p><br>"+fact.text

        elif "remind me to" in userText:
            import re
            userText = userText.replace("remind me to", "").lstrip()
            pattern = re.compile(r"\d\d-\d\d-\d\d \d\d:\d\d")
            dates = re.findall(pattern, userText)
            if len(dates) == 0:
                return "Invalid time input! It must be in the `DD-MM-YY HH:MM` format."

            time = dates[0]
            reminder = userText.replace(time, "").lstrip().rstrip()

            add_reminder(reminder, time)
            return f"Reminder '{reminder}' for {time} added successfully!"
        
        elif "help" in userText:
            import webbrowser
            webbrowser.get().open_new_tab("https://github.com/amalthomas-exe/Wall-E#readme")

        elif "weather" in userText:
            from requests import get as rget
            from json import loads as jloads
            place = userText.replace("weather", "").lstrip()
            url = f"http://api.weatherapi.com/v1/current.json?key=2f081a6878a747a5be135553200709&q={place.capitalize()}"

            try:
                r = rget(url).text
                a = jloads(r)

                current_weather = a.get('current')
                condition = current_weather['condition']
                text = condition['text']

                if current_weather['is_day'] == 0:
                    return f"It is currently night in {place} with current temperature being{current_weather['temp_c']}, though it feels like {current_weather['feelslike_c']}. The weather condition in {place} is {text}."

                elif current_weather['is_day'] == 1:
                    return f"It is currently day in {place} with current temperature being{current_weather['temp_c']}, though it feels like {current_weather['feelslike_c']}. The weather condition in {place} is {text}."

                else:
                    return "An unknown error occured!"

            except Exception as e:
                print(e)
                return "Some error occured!"

        else:
            try:
                import wolframalpha
                client = wolframalpha.Client("UXJ7K4-27QR8YUARX")
                lst.clear()
                return next(client.query(userText).results).text
                
            except:
                import pywhatkit
                pywhatkit.search(userText)
                lst.clear()
                return "Sorry. I do not have the answer to your query, so I'm searching the web for the answer ."

else:
    @app.route("/")
    def no_connection():
        return render_template("not-connected.html")

def run_server():
        print("Server started")
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()

def on_close():
        t2.kill()
        
if __name__ == "__main__":
    multiprocessing.freeze_support()
    p1 = Process(target=check_reminder)
    p1.start()
    print("Thread started")
    t2 = multiprocessing.Process(target=run_server)
    t2.start()
    window = webview.create_window("Wall-E","http://localhost:5000")
    window.closing += on_close
    end = time.time()
    print(f"It took {end-start:.2f} seconds to complete")
    webview.start()
