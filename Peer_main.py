import sys, peers, socket, random

if __name__ == "__main__":
    with open("items_list.txt") as f:
        item_list = [item for item in f.readlines()]
    
    peer = peers.Peer(socket.gethostname(), *sys.argv[1:])
    peer.connect_central(socket.gethostname(), 7890)
    peer.seller_inventory = random.choices(item_list, k=25)
    # print(peer.seller_inventory)  # instead of printing what items to buy lets just make seller search for a random item 
    # and then central server will search for it.

    ch = int(input("What would you like to do?\n1.Buy Item\n2.Add Item to Sell\nEnter : "))
    if ch == 1:
        req_Item = input("What would you like to buy? : ")
        peer.buy_request(req_Item)
    if ch == 2:
        peer.add_item(input("Enter the new item to be sold: "))
