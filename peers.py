import socket, pickle, sys
from socket import AF_INET, SOCK_STREAM


class Peer:
    def __init__(self, ip, peer_port, trade_port) -> None:
        self.ip = ip
        self.pport = int(peer_port)
        self.tport = int(trade_port)
        self.trading_socket = self.create_socket(self.tport)
        self.socket = self.create_socket(self.pport)

        self.seller_inventory = []

    def create_socket(self, port):
        new_socket = socket.socket(AF_INET, SOCK_STREAM)
        new_socket.bind((socket.gethostname(), port))

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
        self.peer_socket.send(
            (f"Connection succesfully established with Peer#{self.pport}").encode()
        )
        self.incoming_central()

    def incoming_central(self):
        while True:
            try:
                query = self.peer_socket.recv(1024).decode()
                if query is not None:
                    if not self.search_inventory(query):
                        self.peer_socket.send(("Negative").encode())

                    self.peer_socket.send(("Positive").encode())
                    # Now listening to the incoming buyer using the trading socket
                    self.incoming_peer()

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
    def sell_request(self, query):
        self.trading_socket.send(f"QUERY {query}")
        while True:
            sellers_list = pickle.load(
                self.trading_socket.recv(1024)
            )
            # seller_ip, port = choose_seller(sellers_list)
            # self.connect_to_seller(seller_ip, port)

    def connect_to_seller(self, ip:str, port:int):
        self.trading_socket.connect((ip, port))
        while True:
            self.trading_socket.send(("Hey do you have dat ting?").encode())
            recvd_message = self.trading_socket.recv(1024).decode()
            print(recvd_message) # maybe print it
            self.trading_socket.close()
            return

if __name__ == "__main__":
    peer = Peer(socket.gethostname(), *sys.argv[1:])
    peer.connect_central()



        
