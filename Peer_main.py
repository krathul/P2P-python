import sys, peers, socket, random

if __name__ == "__main__":
    item_list=[]
    with open('Items.csv') as f:
        item_list=f.readline().split(',')
    
    peer = peers.Peer(socket.gethostbyname('localhost'), *sys.argv[1:])
    peer.connect_central(socket.gethostbyname('localhost'), 7890)
    peer.seller_inventory = random.choices(item_list, k=4)
    print(peer.seller_inventory)

    ch = int(input("What would you like to do?\n1.Buy Item\n2.Add Item to Sell\nEnter : "))
    if ch == 1:
        req_Item = input("What would you like to buy? : ")
        peer.buy_request(req_Item)
    if ch == 2:
        peer.add_item(input("Enter the new item to be sold: "))
