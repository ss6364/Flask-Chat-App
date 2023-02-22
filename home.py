import json
from flask import  Flask, render_template, url_for, redirect, request
from kafka import  KafkaConsumer
from kafka import  KafkaProducer
import pymongo
import datetime
import os
import time
from json import loads, dumps
import threading

app = Flask(__name__)
app.secret_key = 'any random string'


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
user_db = myclient["authentication"]
user_table = user_db["user_info"]

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
users_data = {}
msg_count =  0
"""current_user = None
user_list = []
group_list = []
cid = None # Current user id of chat 
Datastructure : 
{
    "user1" : {
        "cid" : "user2",
        "user_list" : ["user2","user3"], # all the users which are in contact
        "group_list" : ["group1"] # all the roup "cid" is part of
        "msg_list" : {
                    "user2":{
                        "1":{
                            "sender_uid": "user2",
                            "text": "Hi",
                            "timestamp": "11:20 am"
                        },
                        "2":{
                            "sender_uid": "user1",
                            "text": "Hi, user1 ",
                            "timestamp": "11:24 am"
                        },
                    }
        } 
    }
}
users_data={}
users_data{"cid": ,user_list:[],group_list:[],msg_list:{}}
msg_list : {} -> {chat_id:{}}
chat_id: {} -> {msg_id:{"send_uid": ,"text": , "timestamp": }} -> 

"""

""" user handle function """
def user_handle(user_id): # handles data coming from action server consumer
    print("inside useer handle")
    global users_data,msg_count
    consumer = KafkaConsumer(user_id,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    """rec_dict = {
            "op_type":"send",
            "uid1":user_id, #from
            "uid2":chat_id, #to
            "text":text,
            "timestamp":timestamp,
            "msg_id":msg_count,
        }"""
    for msg in consumer:
        print(msg.value)
        rec_dict = msg.value
        if(rec_dict["op_type"]=="send"):
            msg_id = rec_dict['msg_id']
            uid1 = rec_dict["uid1"]
            uid2 = rec_dict["uid2"]
            text = rec_dict["text"]
            timestamp = rec_dict["timestamp"]
            if uid1 not in users_data[user_id]["msg_list"]:
                users_data[user_id]["msg_list"][uid1]={}

            users_data[user_id]["msg_list"][uid1][msg_id] = {} 
            users_data[user_id]["msg_list"][uid1][msg_id]["send_uid"] = uid1
            users_data[user_id]["msg_list"][uid1][msg_id]["text"] = text
            users_data[user_id]["msg_list"][uid1][msg_id]["timestamp"] = timestamp

            #return redirect('/dashboard/'+str(user_id))

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

## Everything related to Registeration here

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route("/register_check", methods=['GET', 'POST'])
def register_check():
    global users_data
    if(request.method == 'POST'):
        req = request.form
        req = dict(req)
        print(req)
         
        query = user_table.find({'uid':req['uid']})
        flag = 0
        for x in query:
            if(x['uid'] == req['uid']):
                flag=1
                break

        reg_dict = {
            "uid": req['uid'],
            "email": req['email'],
            "password": req['password'],
        }

        if(flag == 0):
            temp = user_table.insert_one(reg_dict)
            uid = req['uid']
            
            users_data[uid]={}
            users_data[uid]['cid'] = None
            users_data[uid]['user_list'] = []
            users_data[uid]['group_list'] = []
            users_data[uid]['msg_list'] = {}

            t1=threading.Thread(target=user_handle, args=(uid, ))
            t1.start()

            return redirect('/dashboard/'+str(uid))
        else:
            return render_template("invalid.html", message = "User already registered")    
        
    return render_template("register.html")

## register ends here

## everything related to login startes here

@app.route("/login",  methods=['GET', 'POST'])
def login():
    return render_template("Login.html")

@app.route("/login_check", methods=['GET', 'POST'])
def login_check():
    global users_data
    if(request.method == 'POST'):
        req = request.form
        req = dict(req)
        print(req)
         
        query = user_table.find({'uid':req['uid']})
        flag = 0
        temp = None
        for x in query:
            if(x['uid'] == req['uid']):
                flag=1
                temp = x
                break

        if(flag == 1):
            if(temp["password"]== req["password"]):
                uid = req['uid']
                users_data[uid]={}
                users_data[uid]['cid'] = None
                users_data[uid]['user_list'] = []
                users_data[uid]['group_list'] = []
                users_data[uid]['msg_list'] = {}
                print(uid," Logged in ")
                t1=threading.Thread(target=user_handle, args=(uid,))
                t1.start()
                return redirect('/dashboard/'+str(uid))
            else :
                return render_template("invalid.html", message = "incorrect password")    
        else:
            return render_template("invalid.html", message = "User not registered")    
        
    return render_template("login.html")

## Login ends here


## Dashboard starts here 

# Fetch User
@app.route("/fetch_user/<string:user_id>", methods=['GET', 'POST'])
def fetch_user(user_id):
    global users_data
    file = open("users.txt","r")
    data = file.readlines()
    users_data[user_id]['user_list'] = data
    return redirect('/dashboard/'+str(user_id))

#  Fetch Group 
@app.route("/fetch_group/<string:user_id>", methods=['GET', 'POST'])
def fetch_group(user_id):
    global users_data
    file = open("group.txt","r")
    data = file.readlines()
    users_data[user_id]['group_list'] = data
    return redirect('/dashboard/'+str(user_id))



@app.route("/dashboard/<string:user_id>",  methods=['GET', 'POST'])
def dashboard(user_id):
    global users_data
    chat_id = users_data[user_id]['cid']
    if chat_id != None:
            chat_id = chat_id.strip()  #user1\n
    
    if user_id in users_data:
        if chat_id in users_data[user_id]['msg_list']:
            return render_template('dashboard.html',
                                    uid = user_id,
                                    cid = users_data[user_id]['cid'],
                                    user_list = users_data[user_id]['user_list'],
                                    group_list = users_data[user_id]['group_list'],
                                    msg_list = users_data[user_id]['msg_list'][chat_id],)
        else:
            return render_template('dashboard.html',
                                    uid = user_id,
                                    cid = users_data[user_id]['cid'],
                                    user_list = users_data[user_id]['user_list'],
                                    group_list = users_data[user_id]['group_list'],
                                    msg_list = {})


    return render_template("/home")


## Dashboard ends here


@app.route('/update_cid/<string:user_id>/<string:chat_id>', methods=['GET', 'POST'])
def update_cid(user_id, chat_id):
    global users_data
    #global users_data
    users_data[user_id]['cid'] = chat_id
    return redirect("/dashboard/"+str(user_id))


@app.route("/send_msg/<string:user_id>", methods=['GET','POST'])
def send_msg(user_id):
    global users_data, msg_count, producer
    if (request.method == 'POST'):
        req = request.form
        req = dict(req)
        print(req)
        text = req['typed_msg']
        chat_id = users_data[user_id]['cid']
        if chat_id != None:
            chat_id = chat_id.strip()  #user1\n
        msg_count += 1
        timestamp = str(datetime.datetime.now())
        ## dictionary for kafka
        dict_msg = {
            "op_type":"send",
            "uid1":user_id,
            "uid2":chat_id,
            "text":text,
            "timestamp":timestamp,
            "msg_id":msg_count,
        }

        topic = "ActionServer"
        producer.send(topic, json.dumps(dict_msg).encode('utf-8'))
        print(" Dict_msg : ",dict_msg) ##working fine
        if chat_id in users_data[user_id]['msg_list']:
            users_data[user_id]['msg_list'][chat_id][msg_count] = {}
            users_data[user_id]['msg_list'][chat_id][msg_count]['text'] = text
            users_data[user_id]['msg_list'][chat_id][msg_count]['send_uid'] = user_id
            users_data[user_id]['msg_list'][chat_id][msg_count]['timestamp'] = timestamp    
        else:
            users_data[user_id]['msg_list'][chat_id] = {}

            users_data[user_id]['msg_list'][chat_id][msg_count] = {}
            users_data[user_id]['msg_list'][chat_id][msg_count]['text'] = text
            users_data[user_id]['msg_list'][chat_id][msg_count]['send_uid'] = user_id
            users_data[user_id]['msg_list'][chat_id][msg_count]['timestamp'] = timestamp
        
    return redirect('/dashboard/'+str(user_id))

# Logout
@app.route("/logout/<string:user_id>", methods=['GET', 'POST'])
def logout(user_id):
    global users_data
    print("logout", user_id)
    users_data.pop(user_id)
    return redirect('/home')


# ip : Localhost (127.0.0.1) and port 5000
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
