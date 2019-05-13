import socket 
from _thread import * 
import sys 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
multicast_group = '224.3.29.71' 
server_address = ('', 5000) 
 
server_ip = multicast_group 
 
try: 
    s.bind(server_address) 
    group = socket.inet_aton(multicast_group) 
    mreq = struct.pack('4sL', group, socket.INADDR_ANY) 
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) 
 
except socket.error as e: 
    print(str(e)) 
 
s.listen(2) 
print("Waiting for a connection") 
 
currentId = "0" 
pos = ["0:50,50", "1:100,100"] 
def threaded_client(conn): 
    global currentId, pos 
    conn.send(str.encode(currentId)) 
    currentId = "1" 
    reply = '' 
    while True: 
        try: 
            data = conn.recv(2048) 
            reply = data.decode('utf-8') 
            if not data: 
                conn.send(str.encode("Goodbye")) 
                break 
            else: 
                print("Recieved: " + reply) 
                arr = reply.split(":") 
                id = int(arr[0]) 
                pos[id] = reply 
 
                if id == 0: nid = 1 
                if id == 1: nid = 0 
 
                reply = pos[nid][:] 
                print("Sending: " + reply) 
 
            conn.sendall(str.encode(reply)) 
        except: 
            break 
 
    print("Connection Closed") 
    conn.close() 
 
while True: 
    conn, addr = s.accept() 
    print("Connected to: ", addr) 
 
    start_new_thread(threaded_client, (conn,))