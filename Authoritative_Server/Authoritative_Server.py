import json
import dill
import os
import socket

localIP = "127.0.0.1"
localPort = 53533
bufferSize = 1024
def_type = "A"
    

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    msg_bytes = bytesAddressPair[0]
    client_addr = bytesAddressPair[1]
    
    clientMsg = dill.loads(msg_bytes)
    print("Message from Client:{}".format(clientMsg))

    response = ""

    # If anything is received in an unexpected format
    if len(clientMsg)!=4 and len(clientMsg)!=2:
        print("Invalid request")
        response = "ERROR 400: Invalid request"
        response_bytes = dill.dumps(response)
        UDPServerSocket.sendto(response_bytes, client_addr)


    # Registration by Fibonacci Server to Authoritative server
    if len(clientMsg)==4:
        name, value, type, ttl = clientMsg
        
        if not os.path.exists("AS_records.json"):
            with open("AS_records.json", "w") as file:
                json.dump({}, file, indent=4)
            
        new_record = {}        
        new_record[name] = (value, type, ttl)

        with open("AS_records.json", "w") as file:
            json.dump(new_record, file, indent=4)            

        print("Record saved")
        response_bytes = dill.dumps("Registration Successful")
        UDPServerSocket.sendto(response_bytes, client_addr)

    # Request made by user server
    if len(clientMsg)==2:
        request_type, name = clientMsg          

        with open("as_records.json", "r") as file:
            records = json.load(file)

        if name in records:
            (value, record_type, ttl) = records[name]  
            response_code = 200             
            response = (name, value, response_code)            

            if (type!=request_type):
                print("Invalid type")
                response_code = 400
                response = (name, value, response_code)                 

            print("DNS record provided")

        else:
            print("No record for ", name)
            response = "Record not found"                               

        response_bytes = dill.dumps(response)
        UDPServerSocket.sendto(response_bytes, client_addr)    
        