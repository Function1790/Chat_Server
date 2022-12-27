import threading as td
import lib.createToken as ct
import json
import typing

# 로그


def Log(title, content):
    print(f"[{title}] >> {content}")

# 커멘드 형태로 Dump


def Command_Dump(_cmd, _arg) -> dict:
    return {"Command": _cmd, "Arg": _arg}

# 클라이언트 접속시 객체로 전환


class User:
    # 초기화
    def __init__(self, client):
        self.client = client
        # 토큰 생성 : (객체 고유 아이디 생성)
        self.token = ct.Create_Token(8)
        self.name = "guest"
        self.thread_receive = td.Thread(target=self.Receive_Handle)
        self.thread_receive.daemon = True
        self.thread_receive.start()

    # 받는 데이터 처리
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

            except Exception as e:
                Log("Except", f"{self.getInfo()} Receive_Handle")
                print(e)
                break
        Log("Exit", f"{self.getInfo()}")
        self.client.close()

    # 명령 전송
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

    # 클라언트로 데이터 전달
    def Send(self, text):
        """클라이언트에게 전송"""
        if text == "":
            return False
        #Log("Send", f"{self.getInfo()}  {text}")
        self.client.sendall(text.encode("utf-8"))

    def getInfo(self):
        return f"Client<{self.token}, {self.name}>"


class UserList(typing.List[User]):
    def Chat(self, sender: User, text: str):
        print(f"{sender.name} : {text}")
        for i in self:
            i.Send(f"{sender.name} : {text}")
        return True


# 클라이언트를 담는 리스트
clients = UserList()
