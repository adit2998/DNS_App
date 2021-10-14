import requests

# Program to register the fibonacci server with authoritative server
res = requests.put('http://localhost:9090/register',
                    json={
                    "hostname": "fibonacci.com",
                    "fs_ip": "127.0.0.1",
                    "fs_port":9090,
                    "as_ip": "127.0.0.1",
                    "as_port": 53533,
                    "ttl": 10 })