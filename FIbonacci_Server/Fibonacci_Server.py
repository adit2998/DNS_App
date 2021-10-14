import flask
import requests
import json
import socket
import dill

app = flask.Flask(__name__)

@app.route('/')
def homepage():
    return 'Fibonacci Server'

def findfibo(num):
    a = 0
    b = 1
    if num < 0:
        return -1
         
    elif num == 0:
        return 0
           
    elif num == 1:
        return b
    else:
        for _ in range(1, num):
            c = a + b
            a = b
            b = c
        return b

@app.route('/fibonacci')
def fibonacci():
    num = flask.request.args.get('number')
    if findfibo(int(num))<0:
        return 'Please enter valid number'
    else:
        return 'Fibonacci of '+num+' is '+str(findfibo(int(num)))     
    

@app.route('/register', methods=['PUT'])
def register():
    body = flask.request.json
    print(body)
    if not body:
        return "Body is empty"
    
    hostname = body["hostname"]
    fs_ip = body["fs_ip"]
    as_ip = body["as_ip"]
    as_port = body["as_port"]
    ttl = body["ttl"]
    
    
    msgFromFibo = ((hostname, fs_ip, "A", ttl))
    bytesToSend = dill.dumps(msgFromFibo)
    server_addr = (as_ip, as_port)
    bufferSize  = 1024
    udp_fibo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_fibo_socket.sendto(bytesToSend, server_addr)

    msgFromServer = udp_fibo_socket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])   

    print(msg)
    return "FIbonacci Registration Successful"


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
