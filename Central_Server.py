import socket
import threading
import pickle
import time

class Central:
    def __init__(self, port:int):
        self.Ledger = []
        self.seller_list = []
        self.buyer_list =[]
        self.Socket = self.Create_Socket(port)

    def Create_Socket(self,port_no):
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ServerSocket.bind((socket.gethostbyname('localhost'), port_no))
        return ServerSocket

    def Search_Peer(self, Item, client_addr):
            peer:socket.socket
        
            for peer,addr in self.Ledger:
                if addr != client_addr:
                    peer.send(("QUERY " + Item).encode())
            
            time.sleep(2)
            if len(self.seller_list) == 0: return None
            
            sl_bin = pickle.dumps(self.seller_list)  # CONVERTS PYTHON OBJ TO BYTES
            return sl_bin

    def Communicate(self, client_socket:socket.socket, client_addr):
        #
        while True:
            message = client_socket.recv(1024).decode()
            message=message.split()
            if message[0] == "QUERY":
                self.buyer_list.append((client_socket,client_addr))
                self.seller_list.clear()
                sl_bin=self.Search_Peer(message[1], client_addr)
                if sl_bin==None:
                    client_socket.send("Item Not Found".encode())
                else:
                    client_socket.send("Send list".encode())
                    time.sleep(1)
                    client_socket.send(sl_bin)
                    chosen_seller:socket.socket
                    ch = int(client_socket.recv(1024).decode())
                    chosen_seller = self.Ledger[1][0]
                    chosen_seller.send("Trade".encode())

            elif message[0] == "Trade":
                    print("initiate the trade")
                    seller_tport = message[1]
                    buyer_socket = self.buyer_list[0][0]
                    buyer_socket.send(seller_tport.encode())

            elif message[0] == "Positive":
                        self.seller_list.append(client_addr)

    def Awaken(self):
        self.Socket.listen(10)
        while True:
            # accept connections from outside
            (clientsocket, address) = self.Socket.accept()
            self.Ledger.append((clientsocket,address))
            print("Connection established with #", address[0],address[1])
            # 
            threading.Thread(target = self.Communicate,args = (clientsocket,address)).start()

