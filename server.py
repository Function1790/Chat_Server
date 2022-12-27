import socket as sk
import lib.ManageClient as mc
from lib.ManageClient import clients


#Constant
HOST = "127.0.0.1" 
PORT = 508

#로그
def Log(title, content):
    print(f"[{title}] >> {content}")

#Main
main_server=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
Log("Start", f"PORT : {PORT}, HOST : {HOST}")

main_server.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
main_server.bind((HOST, PORT))
main_server.listen(100)

while True:
    n=len(clients)
    client, addr = main_server.accept()
    clients.append(mc.User(client))

#{"Command":"login", "Arg":"{"uid":"{uid}","upw":"{upw}"}"}

#[Except] >> Client<ahev1gkyj9> Receive_Handle
#Expecting ',' delimiter: line 1 column 30 (char 29)