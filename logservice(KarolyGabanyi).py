#!/usr/bin/python

"""
This application is a "Log service".
The program can started by running this file:
python main.py

Requirements of the program:
-tornado
-requests
Can be installed with pip. Important commands below

After the program starts, it will be created a webserver.
Also a thread will started. This thread sends automatically log messages
to the webserver. The webserver will handle this requests.
The logs can be sended by post messages with a JSON object.
The JSON object should contain all of this attributes paired with a string value:
-id  
-date    
-from    
-to  
-level   
-message

The program write print messages to the output.
This helps the tracking of the running program.

The user can view the stored logs here:
http://localhost:8888/

The program can be configured by these values:
-APP_TOKEN
-ThreadSleepSeconds

The APP_TOKEN is checked by the request handling. 
If it is correct, the log will be stored. Otherwise not.

The ThreadSleepSeconds is necessary because of the test Thread sleeping time.

Written by
Karoly Gabanyi

"""

#Install requirements for the application
#python -m pip install -U pip
#python -m pip install tornado
#python -m pip install requests

import datetime
import json
import tornado.ioloop
import tornado.web

import requests
import time
from threading import Thread
import tornado

import urllib


APP_TOKEN='0000'
ThreadSleepSeconds=2

#Array for storing the logs
#(Instead of a database)
logs=[]

# If the page is requested
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #Variable for storing the full HTML text
        StringForShow=""

        #The beginning of the HTML
        HTMLStringBegin="""
        <html>
        <head>
        </head>

        <body>
            <h1>Logs:</h1>
            <table border="1" cellpadding="5">
                <tr>
                    <th>id</th>
                    <th>date</th>
                    <th>from</th>
                    <th>to</th>
                    <th>level</th>
                    <th>message</th>
                </tr>
        """

        #The end of the HTML
        HTMLStringEnd="""
            </table>
        </body>
        </html>
        """

        StringForShow=StringForShow+HTMLStringBegin

        # Get the last 10 sended log and put into the HTML table
        for log in logs[-10:]:
            StringTemp="""
            <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
                <td>{5}</td>
            </tr>
            """.format(
                    log["id"],
                    log["date"], 
                    log["from"], 
                    log["to"], 
                    log["level"], 
                    log["message"]
                    )

            StringForShow=StringForShow+StringTemp

        StringForShow=StringForShow+HTMLStringEnd
        self.write(StringForShow)

#Handling the sended logs
class MessageHandler(tornado.web.RequestHandler):
    def post(self):
        #Get the text
        temp_string=self.request.body

        #Handle the escape characters
        data = tornado.escape.url_unescape(temp_string)

        #Convert to JSON
        data=json.loads(data)

        if data["apikey"]==APP_TOKEN:
            #Add an ID based on the length of the "logs" array
            data["json_payload"]["id"]=str(len(logs))

            #Add the new log to the array
            logs.append(data["json_payload"])

            print("Log stored")
        else:
            print("Log not stored (Because of bad API key)")

#Create the Tornado Webserver
#Called by the "createAndListenServer" method
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/send", MessageHandler)
    ])

#Method for sending default test message to the server
def sendDefaultJson():
    data = {}
    data['date'] = str(datetime.datetime.now())
    data['from'] = 'Sender'
    data['to'] = 'Log Server'
    data['level'] = '0'
    data['message'] = 'Test log message'
        
    payload={}
    payload['json_payload']=data
    payload['apikey']=APP_TOKEN
    
    json_payload = json.dumps(payload)    
    r = requests.post('http://localhost:8888/send', data=json_payload)
    
#Thread for sending automatically test messages
class worker(Thread):
    def run(self):
        while(True):
            time.sleep(ThreadSleepSeconds)
            sendDefaultJson()

#Create and set the Tornado webserver
def createAndListenServer():
    app = make_app()
    app.listen(8888)
    print("Server created")
    tornado.ioloop.IOLoop.current().start()
    
#The program start point
if __name__ == '__main__':
    worker().start()
    createAndListenServer()




