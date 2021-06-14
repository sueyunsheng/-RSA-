import socket
import rsa
import hash
import wr_excel as wr
import random
import rsa_model

dic = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'


def create_KEY():
    key = ''
    for i in range(16):
        key += random.choice(dic)
    return key

def create_SEED():
    seed = ''
    for j in range(random.randint(20, 30)):
        seed += random.choice(dic)
    return seed

def enroll(client_socket, tcp_server):
    data = ''
    recv_data = client_socket.recv(2048)
    data += recv_data.decode('utf8')
    data = data.split('||')
    uid = data[0]
    pwd = data[1]
    if not wr.read_from_users(uid):
        N = 100
        seed = create_SEED()
        p = pwd + seed
        p = hash.md5_N(p, N)
        N -= 1
        key = create_KEY()
        data = [uid, p, seed, N, key]
        wr.wr_to_users(data)
        print('注册完成')
        client_socket.send('eroll has finished'.encode('utf8'))
    else:
        print('该用户已存在')
        client_socket.send('uid is existed.'.encode('utf8'))


def login(client_socket, tcp_server):
    data = ''
    recv_data = client_socket.recv(2048)
    data += recv_data.decode('utf8')
    data = data.split('||')
    uid = data[0]
    client_e = data[1]
    client_n = data[2]
    print(uid)
    print(client_e)
    print(client_n)
    (client_PKS, pp) = rsa.newkeys(1024)
    client_PKS.e = int(client_e)
    n = int(client_n)
    client_PKS.n = n
    if not wr.read_from_users(uid):
        client_socket.send('UID not in database.')
    else:
        PKS, SKS = rsa_model.create_rsa_key()
        pwd, seed, N, key = wr.read_users(uid)
        M = str(N) + "||" + seed + "||" + pwd + "||" + key
        PK = str(PKS.e) + "||" + str(PKS.n)
        print(M)
        M = rsa_model.encrypt(M.encode('utf8'), client_PKS)
        print(M)
        client_socket.send(M)
        recv_data = client_socket.recv(1024)
        if recv_data == b'ok':
            print("发送加密信息成功")
        else:
            print("error")

        client_socket.send(PK.encode('utf8'))
        recv_data = client_socket.recv(1024)
        if recv_data == b'okk':
            print("服务器密钥发送成功")
        else:
            print("error")
        N = str(int(N) - 1)
        wr.wr_N(uid, N)
        recv_data = client_socket.recv(2048)
        print(recv_data)
        recv_data = rsa_model.decrypt(recv_data,SKS)
        print(recv_data)

        # print(message)
        tmp = hash.md5_once(recv_data)
        print(tmp)
        if pwd == tmp:
            print('认证成功')
            wr.wr_to_pwd(uid, recv_data)
        else:
            print('认证失败')
