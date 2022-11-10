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
        ServerSocket.bind((socket.gethostname(), port_no))
        return ServerSocket
    
    def Search_Peer(self, Item, client_socket):
        peer:socket.socket
        seller_list=[]
        for peer,addr in self.Ledger:
            print(peer, client_socket)
            if peer != client_socket:
                print("Searching on ",addr[0]," ",addr[1])
                peer.send(Item.encode())
                if peer.recv(1024).decode().upper() == "POSITIVE":
                    seller_list.append(addr)
        
        if len(seller_list) == 0: return None
        
        sl_bin = pickle.dumps(seller_list)  # CONVERTS PYTHON OBJ TO BYTES
        return sl_bin

    def Communicate(self, client_socket:socket.socket, _):
        while True:
            message = client_socket.recv(1024).decode()
            print(message)
            if message.split()[0] == "QUERY":
                sl_bin=self.Search_Peer(message.split()[1], client_socket)
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
            self.Ledger.append((clientsocket,address))
            # 
            threading.Thread(target = self.Communicate,args = (clientsocket,"")).start()

