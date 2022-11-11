import socket, pickle, threading, time
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
        new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        threading.Thread(target = self.incoming_central).start()

    def incoming_central(self):
        while True:
            try:
                query = self.peer_socket.recv(1024).decode()
            
                if query is not None:
                    query = query.split()
                    if query[0] == "QUERY":
                        if not self.search_inventory(query[1]):
                            self.peer_socket.send(("Negative").encode())
                        else:
                            self.peer_socket.send(("Positive").encode())
                    
                    elif query[0] == "Trade":
                        print("Enter Trade")
                        # Now listening to the incoming buyer using the trading socket
                        self.trading_socket.listen(1)
                        print("Listening for incoming buyer")
                        self.peer_socket.send(("Trade "+str(self.tport)).encode())
                        connection_socket, addr = self.trading_socket.accept()
                        print("Established connection with the buyer")
                        connection_socket.send("Let's Trade".encode())
                        message = connection_socket.recv(1024).decode()
                        print(message)
                        connection_socket.send(("!!!Item Bought!!!").encode())
                        self.trading_socket.close()
                        print("Trading Done\n\n\n")
                        self.peer_menu()

                    elif query[0] == "Negative":
                        print("!!!Item not found!!!\n\n\n")
                        self.peer_menu()

                    elif query[0] == "Positive":
                        sellers_list = pickle.loads(self.peer_socket.recv(1024))
                        print("Found the following peers")
                        for ip,port in sellers_list:
                            print(ip, port)
                        ch = input("Choose the seller : ")
                        self.peer_socket.send(ch.encode())
                        seller_ip = sellers_list[0]
                        port = int(self.peer_socket.recv(1024).decode())
                        time.sleep(1)
                        self.connect_to_seller(seller_ip[0], port)


            except KeyboardInterrupt:
                self.socket.close()
                return

    # used for forwarding purchase message
    def buy_request(self, query):
        self.peer_socket.send(f"QUERY {query}".encode())

    def connect_to_seller(self, ip:str, port:int):
        self.trading_socket.connect((ip, port))
        while True:
            print("Connection established with the seller")
            print(self.trading_socket.recv(1024).decode())
            self.trading_socket.send(("Let's Trade").encode())
            recvd_message = self.trading_socket.recv(1024).decode()
            print(recvd_message)
            print("\n\n\n")
            self.trading_socket.close()
            self.peer_menu()
            return

    def peer_menu(self):
        ch = int(input("What would you like to do?\n1.Buy Item\n2.Add Item to Sell\nEnter : "))
        if ch == 1:
            req_Item = input("What would you like to buy? : ")
            self.buy_request(req_Item)
        if ch == 2:
            self.add_item(input("Enter the new item to be sold: "))