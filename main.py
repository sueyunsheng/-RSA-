import socket
import connect as con

if __name__ == "__main__":
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('', 8888)
    tcp_socket.bind(address)
    print("开始连接...")
    tcp_socket.listen(5)
    while True:
        client_socket, clientaddr = tcp_socket.accept()
        data = ''
        recv_data = client_socket.recv(2048)
        data += recv_data.decode('utf8')
        print(data)
        if data == "enroll":
            print("开始注册")
            client_socket.send('ok'.encode('utf8'))
            con.enroll(client_socket, tcp_socket)
        elif data == "login":
            print("登录")
            client_socket.send('ok'.encode('utf8'))
            con.login(client_socket, tcp_socket)
        client_socket.close()
    tcp_socket.close()