import socket as sk
import lib.ManageClient as mc
from lib.ManageClient import clients


# Constant
HOST = "127.0.0.1"
PORT = 508

# 로그


def Log(title, content):
    print(f"[{title}] >> {content}")


# Main
# 서버 시작
main_server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
Log("Start", f"PORT : {PORT}, HOST : {HOST}")

# 클라이언트 접속 대기
main_server.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
main_server.bind((HOST, PORT))
main_server.listen(100)

while True:
    n = len(clients)
    # 클라이언트 접속 허가
    client, addr = main_server.accept()
    # User 객체로 클라이언트 추가
    clients.append(mc.User(client))

# Debug Log
# {"Command":"login", "Arg":"{"uid":"{uid}","upw":"{upw}"}"}

#[Except] >> Client<ahev1gkyj9> Receive_Handle
# Expecting ',' delimiter: line 1 column 30 (char 29)
