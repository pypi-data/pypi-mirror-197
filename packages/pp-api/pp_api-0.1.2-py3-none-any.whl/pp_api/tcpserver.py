import socketserver

# Define your request handler class here
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Handle incoming requests here
        data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {data}")
        # send a response back to the client
        # self.request.sendall(b"Hello, client!")
        self.request.sendall(data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

