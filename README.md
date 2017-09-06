# Logservice

This application is a "Log service".
The program can started by running this file:
python main.py
Requirements of the program:
- tornado
- requests

Can be installed with pip. Important commands below
After the program starts, it will be created a webserver.
Also a thread will started. This thread sends automatically log messages
to the webserver. The webserver will handle this requests.
The logs can be sended by post messages with a JSON object.
The JSON object should contain all of this attributes paired with a string value:
- id  
- date    
- from    
- to  
- level   
- message

The program write print messages to the output.
This helps the tracking of the running program.
The user can view the stored logs here:
http://localhost:8888/

The program can be configured by these values:
- APP_TOKEN
- ThreadSleepSeconds

The APP_TOKEN is checked by the request handling. 

If it is correct, the log will be stored. Otherwise not.
The ThreadSleepSeconds is necessary because of the test Thread sleeping time.

Written by </br>
Karoly Gabanyi
