# -*- coding: utf-8 -*-
import socket
import base64
import rsa
import hashlib


def uid_rsakeys(uid):
    hash = hashlib.md5()  # 创建了一个md5算法的对象(md5不能反解)，即造出hash工厂
    hash.update(bytes('password', encoding='utf-8'))  # 运送原材料喽，要对哪个字符串进行加密，就放这里
    ret_hash = hash.hexdigest()  # 产出hash值,拿到加密字符串
    (pku, sku) = rsa.newkeys(1024)
    return ret_hash, pku, sku


def otp(seed, pwd, N):
    message = pwd + seed
    for i in range(N):
        message = message.encode('utf-8')
        message = hashlib.md5(message).hexdigest()
        temp = i+1
        print("第%s次:" % temp, message)
    return message


def decode_rsa(crypto, sku):
    # 私钥解密
    content = rsa.decrypt(crypto, sku)
    con = content.decode("utf-8")
    return con


def encode_rsa(content, pku):
    content = content.encode("utf-8")
    # 公钥加密
    crypto = rsa.encrypt(content, pku)
    return crypto


def process_enroll(uid, pwd, dest_ip, dest_port):
    print("开始enroll")
    huid, pku, sku = uid_rsakeys(uid)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_addr = (dest_ip, dest_port)
    tcp_socket.connect(dest_addr)
    print("准备发送数据")
    # enroll
    send_data = "enroll"
    tcp_socket.send(send_data.encode("utf-8"))
    print("发送:", send_data.encode('utf-8'))
    # 接收服务器发送的数据
    recv_data = tcp_socket.recv(1024).decode("utf-8")
    print("接收:", recv_data)
    if recv_data == 'ok':
        send_data = str(huid) + '||' + str(pwd)
        tcp_socket.send(send_data.encode("utf-8"))
        print("发送:", send_data.encode('utf-8'))
        recv_data = tcp_socket.recv(1024).decode("utf-8")
        print("接收:", recv_data, "注册完成")
    # else:
    #     recv_data = tcp_socket.recv(1024).decode("utf-8")
    #     print("接收:", recv_data, "已经存在")
    #     tcp_socket.close()
    # 4. 关闭套接字socket
    tcp_socket.close()


def process_login(uid, pwd, dest_ip, dest_port):
    print("开始login")
    huid, pku, sku = uid_rsakeys(uid)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_addr = (dest_ip, dest_port)
    tcp_socket.connect(dest_addr)

    # login
    send_data = "login"
    tcp_socket.send(send_data.encode("utf-8"))
    # 接收服务器发送的数据
    recv_data = tcp_socket.recv(1024)
    print("接收:", recv_data.decode("utf-8"))
    if recv_data.decode("utf-8") == 'ok':
        send_data = str(huid) + '||' + str(pku.e) + '||' + str(pku.n)
        tcp_socket.send(send_data.encode("utf-8"))
        print("发送:", send_data.encode('utf-8'))
        recv_data = tcp_socket.recv(1024)
        recv_data = decode_rsa(recv_data, sku)
        print("接收m1", recv_data)
        tcp_socket.send('ok'.encode("utf-8"))
        print("发送:", 'ok'.encode('utf-8'))
        recv_data2 = tcp_socket.recv(1024)
        print("接收m2", recv_data2)
        tcp_socket.send('okk'.encode("utf-8"))
        print("发送:", 'okk'.encode('utf-8'))
        if recv_data == 'UID not in database':
            print('UID not in database')
            tcp_socket.close()
        else:
            data = recv_data.split('||')
            data2 = recv_data2.decode('utf-8').split('||')
            print("data:", data)
            N, seed, fn0, key, e, n = int(data[0]), data[1], data[2], data[3], data2[0], data2[1]
            (pks, sks) = rsa.newkeys(1024)
            pks.e = int(e)
            pks.n = int(n)
            print("pks:", pks)
            fn = otp(seed, pwd, N)
            fm = otp(seed, pwd, int(N) + 1)
            print("fn:", fn, "fm:", fm)
            if fm == fn0:
                print("服务器验证成功")
                send_data = encode_rsa(str(fn), pks)
                tcp_socket.send(send_data)
                tcp_socket.close()
                print("发送:", send_data)
            else:
                print('服务器验证不成功')
                tcp_socket.close()


if __name__ == '__main__':
    # uid = input("请输入你的用户名-uid")
    # pwd = input("请输入你的密码-pwd")
    uid, pwd = "admin", "12345"
    print(uid, pwd)
    hu, pku, sku = uid_rsakeys(uid)
    print(hu, pku, sku)
    dest_ip = ''
    dest_port = 8888
    process_login(uid, pwd, dest_ip, dest_port)
    exit()
    #
    # otp(123, 456, 20)
    # ciphertext = encode_rsa("hello world", pku)
    # print(ciphertext)
    # print(decode_rsa(ciphertext, sku))
    # print(pku.e, pku.n, pku)
    # (pku1, sku1) = rsa.newkeys(1024)
    # print(pku1)
    # pku1.n = int(pku.n)
    # pku1.e = int(pku.e)
    # print(pku1)
    # print(decode_rsa(encode_rsa("hello world", pku1), sku))
