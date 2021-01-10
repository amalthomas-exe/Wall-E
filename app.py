from flask import Flask, render_template, request
import wolframalpha
import pickle
import random
import webbrowser
from datetime import datetime
import yagmail
from email_validator import validate_email, EmailNotValidError
from urllib.request import urlopen

now = datetime.now()
now2 = now.strftime("%H:%M")
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
    return render_template("index.html",time = now2,User = dict["first-name"])


@app.route("/get")
def get_bot_response():
    ##functions to be defined below this line
    userText = request.args.get('msg')
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
                    except:
                        return "Looks like the provided mail id is not valid. Please check the mail id you have provided. "
        elif ("mail" or "email") in i.lower():
            bot_response.append("mail-without-id")
            return random.choice(["Please specify a mail-id","Please mention the mail-id of the recipient."])
    if bot_response[-1]=="mail-with-id":
        mailer = yagmail.SMTP(dict["email"],dict["password"])
        try:
            mailer.send(mail_addr,"Message from "+dict["first-name"],userText)
            bot_response.clear()
            return random.choice(["Got it! The mail has been sent 👍","The message has been sent 👍","Mail send 👍"])
        except:
            return 'Oops! Looks like I\'m unable to send the mail because Google is blocking me from doing so. Please go to <a href="https://www.google.com/settings/security/lesssecureapps">this link</a> to allow me to send mails'  
    
     if "news" in userText:     #Data scraping from a google
        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = BeautifulSoup(xml_page, "html.parser")
        news_list = soup_page.findAll("item")
        send("Here are top 3 news")
        news = "Here are some news"
        for news in news_list[:3]:
            news = news + "\n" + (news.title.text)
        return news
        
    

if __name__ == "__main__":
    app.run()
