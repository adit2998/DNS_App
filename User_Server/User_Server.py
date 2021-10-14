import flask
import requests
import socket
import dill

bufferSize = 1024

app = flask.Flask(__name__)

@app.route('/')
def user_homepage():
    return 'User Server'


@app.route('/fibonacci', methods=["GET"])
def fibonacci():
    # Get params from request arguments
    hostname = flask.request.args['hostname']
    fs_port  = int(flask.request.args['fs_port'])
    num   = int(flask.request.args['number'])
    as_ip    = flask.request.args['as_ip']
    as_port  = int(flask.request.args['as_port'])

    server_addr = (as_ip, as_port)
    udp_user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg_bytes = dill.dumps(("A", hostname))
    udp_user_socket.sendto(msg_bytes, server_addr)

    # Get response from AS for ip address of fibonacci server
    response, client_ip = udp_user_socket.recvfrom(bufferSize)
    response = dill.loads(response)
    # Unpack values from AS response    
    (name, fs_ip, response_code) = response    
    
    if response_code==400:
        return 'ERROR 400: IP Address for Fibonacci server not found'

    else:
        return requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": num}).content
    

app.run(host='0.0.0.0',
        port=8080,
        debug=True)