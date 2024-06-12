#!/usr/bin/env python
import socket
import os

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        conn, addr = server_socket.accept()  # wait for client
        with conn:
            val = conn.recv(1024)
            if not val:
                break
            pars = val.decode()
            args = pars.split("\r\n")

            if len(args) > 1:
                path = args[0].split(" ")
                if path[1] == "/":
                    response = b"HTTP/1.1 200 OK\r\n\r\n"

                elif path[1].startswith("/echo/"):
                    string = path[1][6:]  # Rimuove "/echo/"
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                elif path[1].startswith("/files/"):
                    fileName = path[1].split("/")[2]
                    filePath = f"/tmp/data/codecrafters.io/http-server-tester/{fileName}"

                    if os.path.isfile(filePath):
                        with open(filePath, "r") as source_file:
                            content = source_file.read()
                            print(content)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
                    else:
                        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                          
                elif path[1].startswith("/user-agent"):
                    userAgent=args[3].split(" ")
                    print(userAgent)
                    string= userAgent[1]
                    print(string)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                else:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"  # Caso predefinito per altri percorsi
                print(f"First par {path}")
            else:
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"  # Risposta per richieste non valide

            print(f"Received: {val}")
            print(response)
            conn.sendall(response)
            

if __name__ == "__main__":
    main()
    