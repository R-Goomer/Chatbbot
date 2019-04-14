from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from werkzeug import secure_filename
import pymysql
import datetime
import os

##initializing variables
s=0
q=0

##preparing chatbot
chatbot = ChatBot('Rushil')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")##training the bot

app = Flask(__name__)

def date_time():                 ##getting date and time
   currentDT = datetime.datetime.now()
   return (str(currentDT)[0:19])
   

def insert_sql(user_input):      ##inserting user inputs, bot outputs and time into database
   global s
   s=s+1
   resp = str(chatbot.get_response(user_input))
   try:
      sql = 'insert into user_bot_chat values('+str(s)+',"' + date_time() + '","'+user_input+'","'+resp+'");'
      a.execute(sql)
      conn.commit()
   except:
      print("Some error in the tables, check if table does exist and its inputs")


def file_names():                ##extracting filenames uploaded earlier from files database
   file_names=[]
   sql = 'select File_name from files;'
   a.execute(sql)
   w_file = list(a.fetchall())
   for i in w_file:
     file_names.append(i[0])
   return(file_names)

def user_list():                 ##extracting user inputs from user_bot_chat database
   user=[]
   sql = 'select User_input from user_bot_chat;'
   a.execute(sql)
   w_user=list(a.fetchall())
   for i in w_user:
      user.append('User: '+i[0])
   return(user)

def bot_list():                  ##extracting bot responses from user_bot_chat database
   bot=[]
   sql = 'select Bot_output from user_bot_chat;'
   a.execute(sql)
   w_bot=list(a.fetchall())
   for i in w_bot:
      bot.append('Bot: '+i[0])
   return(bot)

@app.route('/home')           ##links to the first page - upload.html
def index():
   return render_template("upload.html")

@app.route('/uploader',methods=['GET', 'POST']) ##called when new file is uploaded in UI
def uploader():
   if request.method == 'POST':
      global q
      q=q+1
      f = request.files['file']
      f.save(secure_filename(f.filename))
      path_to_file = "C:/Users/Sumit Manocha/Desktop/IIT-Hyd/"+str(f.filename)
      print("file is saved")
      try:
         sql = 'insert into files values('+str(q)+',"' + date_time() + '","'+str(f.filename)+'","'+ path_to_file +'");'
         a.execute(sql)
         conn.commit()
      except:
         print("Some error in the tables, check if table does exist and its inputs")
   return render_template("index.html",user_input=r(),file_list=file_names())

def r():          ##takes user inputs and bot outputs and insert into a array to later send to html file
   try:
      user_input = request.form["user_input"]
      insert_sql(user_input)
      r=[]
      user = user_list()
      bot = bot_list()
      for j in range(0,len(user)):
         r.append(user[j])
         r.append(bot[j])
      return(r)
   except:
      r=[]
      user = user_list()
      bot = bot_list()
      for j in range(0,len(user)):
         r.append(user[j])
         r.append(bot[j])
      return(r)      
      

@app.route('/process',methods=['POST'])
def process():                ##called when user input is given and submit button is pressed
    return render_template("index.html",user_input=r(),file_list=file_names())


if __name__ == '__main__':
   try:     ##connects to the database
      conn= pymysql.connect(host='localhost',user='root',password='root',db='chat')
      a=conn.cursor()
   except:
      print("connection error - hostname or password incorrect")
   app.run(host='127.10.0.0', port=int('8000'), debug = True)##0.0.0.0.,80
   conn.close()
   a.close()
