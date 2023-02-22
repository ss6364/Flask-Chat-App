## Objective
------------
To make a char app using flask:
1. Register user - completed
2. Login User - completed
3. Send messages - completed
4. Deleting / updating messages - in queue
5. Should support group chat - in queue
6. Chat should be persistant - in progress
--------------------------------------------------------------------------------
Technologies :
--------------------------------------------------------------------------------
Python
Flask
Kafka
MongoDB
HTML
CSS
JavaScript
Bootstrap
--------------------------------------------------------------------------------

Till Now:
1. User can Register & Login
2. User can refresh contacts and groups
3. Send and Receive text messages in real time.
3. User can logout.

To do:
1. Implement Database for messaging history and connect user list and group list to DB
2. Create and Delete Group
3. Admin/control Panel for group
4. Optimize the performance of the app.


---------------------------------------------------------------------------------
Database Connection - Mongo DB
---------------------------------------------------------------------------------
As per now data is stored in real-time in the Dictionary data-structure as shown below:
user Record :
...
```python
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
```

----------------------------------------------------

Running the app : 

>> Use commands in commands.txt to start zookeeper and kafka.
>> in virtual env/ run python home.py
>> in virtual env/ run python action_server.py

----------------------------------------------------

Adding the screenshots for the same:

Flow Diagram:

![Flow Diagram](https://user-images.githubusercontent.com/33020180/220600246-6fed3771-4530-481e-9ca2-26cb41211aa8.png)

Home Page :

![Home_page](https://user-images.githubusercontent.com/33020180/220600307-25cf6b97-bd7f-410a-bcf9-255c5f0c0d5e.png)

Login & Registration :

![Login   Registration page](https://user-images.githubusercontent.com/33020180/220600309-d4b31810-46f9-4335-a549-3b0ae2521b1f.png)

home Screen after Login:

![Home screen after login](https://user-images.githubusercontent.com/33020180/220600297-113fe6e9-d3b4-4d99-8fd7-868d4de999ab.png)

Home Screen after Refreshing Contacts and groups:

![Home Screen after Refreshing Contacts   groups](https://user-images.githubusercontent.com/33020180/220600303-ef4843df-d717-446f-9864-eafd25a17a45.png)

sending and receiving messages
![sending   receiving messages](https://user-images.githubusercontent.com/33020180/220600286-a05083a7-c213-4335-9ff6-d7f8c4ef3438.png)

![Backend Consoles Realtime](https://user-images.githubusercontent.com/33020180/220600114-572d7c80-6ff6-496c-b96e-3fdb4a1d9d50.png)




