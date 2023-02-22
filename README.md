## Objective
------------
To mmake a char app using flask:
1. Register user
2. Login User
3. Send messages
4. Deleting / updating messages
5. Should support group chat
6. Chat should be persistant
--------------------------------------------------------------------------------

# Firtst we will try to create a flask app

# HTML Pages
Home
Login 
Register
dashboard

--------------------------------------------------------------------------------4

# Register form and login form CSS
https://bootsnipp.com/sunil8107?page=1

--------------------------------------------------------------------------------
# Dashboard UI
https://bootsnipp.com/snippets/exR5v


Database Connection
-------------------

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = myclient["authentication"]
user_table = user_db["user_info"]

if(request.method == "POST"):
    req = request.form
    req = dict(req)

# insert a new record
user_table.insert_one(reg_dict)

# query a record
query = user_table.find({'uid':req['uid']})

---------------------------------------------------------------------------------

# User_Record

# user_information
...
**{
    "user1" : {
        "cid" : "user2",
        "user_list" : ["user2","user3"],
        "group_list" : ["group1"]
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
}**

{
    "user2" : {
        "cid" : "user1",
        "user_list" : ["user2","user3"],
        "group_list" : ["group1"]
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

----------------------------------------------------

# Producer:

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
producer.send(topic, json.dumps(dict_msg).encode('utf-8'))

# consumer
consumer = KafkaConsumer(user_id,
bootstrap_servers=['localhost:9092],
auto_offset_reset='latest',
enable_auto_commit=True,
value_deserializer=lambda x: loads(x.decode('utf-8')))