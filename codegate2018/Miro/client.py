from socket import *
from ssl import *
import time

def recv_until(s, string):
    result = ''
    while string not in result:
        result += s.recv(1)
    return result

client_socket=socket(AF_INET, SOCK_STREAM)
tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1_2, cert_reqs=CERT_NONE)

print "[+] Connecting with server.."

tls_client.connect(('ch41l3ng3s.codegate.kr',443))

print "[+] Connect OK"

while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    #message
    user_input = raw_input()
    
    if user_input == "u":
        print "Sorry.. Not support function.."
        exit()
    elif user_input == "d": 
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        print "Sorry.. Not support function.."
        exit()
    else:
        print "Invalid input!"
        exit()    

client_socket.shutdown(SHUT_RDWR)
client_socket.close()