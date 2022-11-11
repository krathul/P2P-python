import sys, peers, socket, random

if __name__ == "__main__":
    item_list=[]
    with open('items_list.txt') as f:
        item_list = f.readlines()
        item_list = list(map(str.strip, item_list))
    
    peer = peers.Peer(socket.gethostbyname('localhost'), *sys.argv[1:])
    peer.connect_central(socket.gethostbyname('localhost'), 7890)
    peer.seller_inventory = random.choices(item_list, k=8)
    print(peer.seller_inventory)
    peer.peer_menu()
