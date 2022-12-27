import socket as sk
import threading as th
import json

HOST = "127.0.0.1"
PORT = 508
AUTO_LOGIN = True

print("[ Client ]")
client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client.connect((HOST, PORT))


def Log(title, content):
    print(f"[{title}] >> {content}")


def Receive_Handle():
    while True:
        try:
            data = client.recv(1024)
            text = data.decode("utf-8")
            if text != "":
                Log("받음", text)
                print(end="\n채팅 >> ")
        except:
            Log("Except", "Error")
            break


def Send(text):
    client.sendall(text.encode("utf-8"))


def Command_Dump(_cmd, _arg):
    return {"Command": _cmd, "Arg": _arg}


#main

# 연결
receive = th.Thread(target=Receive_Handle)
receive.start()
Log("System",f"연결에 성공하였습니다. [연결주소 {HOST}:{PORT}]\n")

# 이름 설정
while True:
    name = input("이름을 입력하세요 >> ")
    if name.replace(" ", "") != "":
        break
    print("\n이름은 공백이 아니어야 합니다.")

set_name_command = Command_Dump("setname", name)
Send(json.dumps(set_name_command))

# 채팅
while True:
    text = input("채팅 >> ")
    chat_command = Command_Dump("chat", text)
    Send(json.dumps(chat_command))

client.close()
