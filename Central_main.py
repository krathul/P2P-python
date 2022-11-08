import sys
import Central_Server

if __name__=="__main__":
    port = int(sys.argv[1])
    Central_node = Central_Server.Central(port)
    print("Central Node Listening on", port)
    Central_node.Awaken()