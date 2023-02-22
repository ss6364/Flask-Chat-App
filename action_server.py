from flask import  Flask, render_template, url_for, redirect, request
from kafka import  KafkaConsumer
from kafka import  KafkaProducer
import pymongo
import datetime
import os
import time
import json
from json import loads, dumps
import threading

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
# rec_dict = received dictionary coming from home.py

def handle_send(rec_dict):
    pass

def consume_message(topic):
    global producer
    consumer = KafkaConsumer(topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: loads(x.decode('utf-8')))

    for msg in consumer:
        print(msg.value)
        rec_dict = msg.value
        if(rec_dict["op_type"] == "send"):
            producer.send(rec_dict['uid2'], json.dumps(rec_dict).encode('utf-8'))
            handle_send(rec_dict)


def main():
    topic = "ActionServer"
    t1 = threading.Thread(target=consume_message, args=(topic, ))
    t1.start()
    t1.join()
    print("Done")

if __name__ == '__main__':
    main()
        