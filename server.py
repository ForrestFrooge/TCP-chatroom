import socket
import threading
import os



class Server():
    def __init__(self,PORT = 40674) -> None:
        self.PORT = PORT

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.log = [b"EOL"]
        self.connections = []

    def start(self):

        self.s.bind(("",self.PORT))
        print("SOCKET BINDED : %s" %(self.PORT))

        self.s.listen(5)
        print("SOCKET LISTENING")

        accept_thread = threading.Thread(target=self.accept)
        accept_thread.start()


    def accept(self):
        while True:
            connection, address = self.s.accept()
            print("CONNECTION ACCEPTED FROM : ",address)


            for i in reversed(self.log):
                connection.send(i + b"\n")
            
            for i in self.connections:
                i.send(bytes(str(address[1]) + " has connected","utf-8"))

            self.connections.append(connection)
            handle_thread = threading.Thread(target=self.handle,args=(connection,address))
            handle_thread.start()

    def handle(self,connection,address):
        try:
            while True:
                try:
                    message = connection.recv(2048)
                    self.log.insert(0,bytes(str(address[1]) + " : ","utf-8") + message)

                    for i in self.connections:
                        i.send(self.log[0])
                    
                    if message == b"/SHUTDOWN":
                        for i in self.connections:
                            i.send(b"/SHUTDOWN")
                        os.abort()

                except OSError:
                    print("Socket error, likely disconnected")
                    self.connections.remove(connection)
                    for i in self.connections:
                        i.send(bytes(str(address[1]) + " has disconnected","utf-8"))
                    connection.close()
                    
        finally:
            connection.close()
            return
            


if __name__ == "__main__":
    server = Server()
    server.start()