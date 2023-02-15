import threading as td
import lib.createToken as ct
import json
import typing

# 로그


def Log(title, content):
    print(f"[{title}] >> {content}")

# 서버로 전송시 프로토콜 규격
# Head : Command, Body : Argument


def Command_Dump(_cmd, _arg) -> dict:
    return {"Command": _cmd, "Arg": _arg}

# 클라이언트 접속시 객체로 전환

# 클라이언트 객체


class User:
    # 생성자
    def __init__(self, client):
        self.client = client
        # 토큰 생성 : (객체 고유 아이디 생성)
        # 36의 8제곱개의 토큰 생성 가능
        self.token = ct.Create_Token(8)
        # 이름 미생성시 guest
        self.name = "guest"
        # 데이터 수신시 thread에서 처리
        self.thread_receive = td.Thread(target=self.Receive_Handle)
        self.thread_receive.daemon = True
        self.thread_receive.start()

    # 수신 받은 데이터 분석 및 처리
    def ProcessData(self, recv_data):
        cmd = recv_data["Command"]
        arg = recv_data["Arg"]
        if cmd == "chat":
            # 모든 유저에게 전송
            clients.Chat(self, arg)
        elif cmd == "setname":
            self.name = arg
            Log("Join", f"{self.getInfo()}")
        return True

    # 클라이언트에서 전송된 데이터를 받는 함수(Thread)
    def Receive_Handle(self):
        while True:
            try:
                data = self.client.recv(1024)
                text = data.decode("utf-8")
                #Log("Get", f"{self.getInfo()} : {text}")
                self.ProcessData(json.loads(text))
            except Exception as e:  # 오류 처리
                Log("Except", f"{self.getInfo()} Receive_Handle")
                print(e)
                break
        Log("Exit", f"{self.getInfo()}")
        self.client.close()

    # 데이터 프로토콜 방식으로 전송
    def SendCmd(self, command):
        if command == "":
            return False
        send_cmd = json.dumps(command)
        try:
            self.client.sendall(send_cmd.encode("utf-8"))
            #Log("Send", f"{self.getInfo()}  {send_cmd}")
        except Exception as e:
            Log("Error", f"{self.getInfo()} SendCmd")
            print(e)

    # 클라이언트로 데이터 전송
    def Send(self, text):
        """클라이언트에게 전송"""
        if text == "":
            return False
        #Log("Send", f"{self.getInfo()}  {text}")
        self.client.sendall(text.encode("utf-8"))

    # 클라이언트 정보 str로 반환
    def getInfo(self):
        return f"Client<{self.token}, {self.name}>"

# 유저 관리 클래스


class UserList(typing.List[User]):
    # 한명이 채팅 전송하면 모두에게 해당 내용 전송
    def Chat(self, sender: User, text: str):
        print(f"{sender.name} : {text}")
        for i in self:
            i.Send(f"{sender.name} : {text}")
        return True


# 클라이언트를 담는 리스트
clients = UserList()
