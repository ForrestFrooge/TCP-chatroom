import socket
import threading 
import os



class Client():
    def __init__(self,HOST = "127.0.0.1",PORT = 40674):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        self.PORT = PORT
        self.HOST = HOST

        self.s.connect((self.HOST, self.PORT))

        self.log = []

    def start(self):
        self.recieve_thread = threading.Thread(target=self.recieve)
        self.send_thread = threading.Thread(target=self.send)

        self.recieve_thread.start()
        self.send_thread.start()

    def recieve(self):
        while True:
            message = self.s.recv(2048)
            self.log.append(message)
            self.display()
            if message == b"/SHUTDOWN":
                self.shutdown()
                
    def display(self):
        os.system("cls" if os.name == "nt" else "clear")
        for message in self.log:
            print(str(message,encoding="utf-8"))

    def send(self):
        try:
            while True:
                message = input("Type message here : ")

                self.s.send(bytes(message,"utf-8"))
        except KeyboardInterrupt:
            self.shutdown()
        except EOFError:
            self.shutdown()

    def shutdown(self):
        try:
            self.s.close()
            os.abort()
        except:
            print("Error closing socket")
        os.abort()



if __name__ == "__main__":
    ip = input("Enter IP (127.0.0.1) : ")
    port = input("Enter port (40674) : ")

    client = Client(ip,port)
    client.start()