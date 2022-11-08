import socket
import threading
import pickle

class Central:
    def __init__(self, port:int):
        self.Ledger = []
        print(port)
        self.Socket = self.Create_Socket(port)

    def Create_Socket(self,port_no):
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ServerSocket.bind((socket.gethostbyname('localhost'), port_no))
        return ServerSocket
    
    def Search_Peer(self, Item):
        peer:socket.socket
        seller_list=[]
        for peer,addr in self.Ledger:
            peer.send(Item.encode())
            if peer.recv(1024).decode() == "POSITIVE":
                seller_list.append(addr)
        
        if len(seller_list) == 0: return None
        
        sl_bin = pickle.dumps(seller_list)  # CONVERTS PYTHON OBJ TO BYTES
        return sl_bin

    def Communicate(self, client_socket:socket.socket, _):
        while True:
            message = client_socket.recv(1024).decode().split()
            print(message)
            if message[0] == "QUERY":
                sl_bin=self.Search_Peer(message[1])
                if sl_bin==None:
                    client_socket.send("Item Not Found".encode())
                else:
                    client_socket.send(sl_bin)
                    chosen_seller:socket.socket
                    chosen_seller = int(client_socket.recv().decode())
                    chosen_seller = self.Ledger[chosen_seller][0]
                    chosen_seller.send("Trade".encode())

    def Awaken(self):
        self.Socket.listen(10)
        while True:
            # accept connections from outside
            (clientsocket, address) = self.Socket.accept()
            print(address, "got connected")
            self.Ledger.append((clientsocket,address))
            # 
            threading.Thread(target = self.Communicate,args = (clientsocket,"")).start()

