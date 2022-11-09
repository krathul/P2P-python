import socket, pickle, threading
from socket import AF_INET, SOCK_STREAM


class Peer:
    def __init__(self, ip, peer_port, trade_port) -> None:
        self.ip = ip
        self.pport = int(peer_port)
        self.tport = int(trade_port)
        self.trading_socket = self.create_socket(self.tport,ip)
        self.peer_socket = self.create_socket(self.pport,ip)

        self.seller_inventory = []

    def create_socket(self, port, ip):
        new_socket = socket.socket(AF_INET, SOCK_STREAM)
        new_socket.bind((ip, port))

        return new_socket

    def search_inventory(self, query: str):
        for item in self.seller_inventory:
            if query in item:
                return True

        return False

    def add_item(self, item: str):
        self.seller_inventory.append(item)

    def connect_central(self, central_ip, central_port):
        self.peer_socket.connect((central_ip, central_port))
        # self.peer_socket.send(
        #     (f"Connection succesfully established with Peer#{self.pport}").encode()
        # )
        threading.Thread(target = self.incoming_central).start()

    def incoming_central(self):
        while True:
            try:
                query = self.peer_socket.recv(1024).decode()
                print(query)
                if query is not None:
                    query = query.split()
                    if query[0] == "QUERY":
                        if not self.search_inventory(query[1]):
                            self.peer_socket.send(("Negative").encode())
                        else:
                            self.peer_socket.send(("Positive").encode())
                            # Now listening to the incoming buyer using the trading socket
                            self.incoming_peer()
                    else:
                        sellers_list = pickle.loads(self.peer_socket.recv(1024))
                        for ip,port in sellers_list:
                            print(ip, port)
                        ch = input("Choose the seller : ")
                        seller_ip, port = sellers_list[ch]
                        self.connect_to_seller(seller_ip, port)


            except KeyboardInterrupt:
                self.socket.close()
                return

    def incoming_peer(self):
        self.trading_socket.listen(1)
        while True:
            connection_socket, addr = self.trading_socket.accept()
            message = connection_socket.recv(1024).decode()
            connection_socket.send(("Positive").encode())
            self.trading_socket.close()
            self.incoming_central()
            self.trading_socket.close()
            return

    # used for forwarding purchase message
    def buy_request(self, query):
        self.peer_socket.send(f"QUERY {query}".encode())

    def connect_to_seller(self, ip:str, port:int):
        self.trading_socket.connect((ip, port))
        while True:
            self.trading_socket.send(("Hey do you have dat ting?").encode())
            recvd_message = self.trading_socket.recv(1024).decode()
            print(recvd_message) # maybe print it
            self.trading_socket.close()
            return

    