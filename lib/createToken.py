import random as r

thex=["0","1","2","3","4","5","6","7","8",
    "9","a","b","c","d","e","f","g","h","i",
    "j","k","l","m","n","o","p","q","r","s",
    "t","u","v","w","x","y","z"]

#Token 생성
def Create_Token(length):
    """Cases : 36**(length)"""
    result=""
    for i in range(length):
        result+=str(thex[r.randint(0,len(thex)-1)])
    return result