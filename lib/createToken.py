import random as r

chars = "abcdefghijklmnopqrstuvwxyz0123456789"

# Token 생성


def Create_Token(length):
    """Cases : 36**(length)"""
    result = ""
    # chars 중에 하나 뽑기
    for i in range(length):
        result += str(chars[r.randint(0, len(chars)-1)])
    return result
