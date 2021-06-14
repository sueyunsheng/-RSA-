from hashlib import md5
import os


def md5_N(message, N):
    for i in range(N):
        message = message.encode('utf8')
        message = md5(message).hexdigest()
    return message

def md5_once(message):
    message = message.encode('utf8')
    message = md5(message).hexdigest()
    return message

# print(md5_once('c8d426dbb466393f934e702fc0153976'))
