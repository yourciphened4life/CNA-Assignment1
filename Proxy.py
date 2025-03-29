import socket
import threading
import re

# Define the proxy server address and port
PROXY_HOST = 'localhost'
PROXY_PORT = 8080

# Function to handle client connections
def handle_client(client_socket):
    """
    Handles an incoming client request by forwarding it to the origin server,
    retrieving the response, and sending it back to the client.
    """
    try:
        # Receive request from the client
        request = client_socket.recv(4096).decode()
        print("Received request:\n", request)

        # Extract the first line to get method and URL
        request_lines = request.split('\r\n')
        first_line = request_lines[0]
        method, url, version = first_line.split()

        # Validate HTTP version
        if not url.startswith("http://") and not url.startswith("https://"):
            print("Invalid URL format")
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nInvalid URL format".encode())
            client_socket.close()
            return
        
        # Remove 'http://' or 'https://' if present and extract hostname and resource
        url = re.sub(r'^http://|^https://', '', url)  # Remove 'http://' or 'https://'
        host_end = url.find('/')
        hostname = url[:host_end] if host_end != -1 else url
        resource = url[host_end:] if host_end != -1 else '/'

        print(f"Forwarding request to {hostname}{resource}")

        # Connect to the origin server
        origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin_socket.connect((hostname, 80))  # Assume HTTP port 80 for simplicity

        # Forward the request to the origin server
        origin_request = f"{method} {resource} {version}\r\n"
        for line in request_lines[1:]:
            origin_request += f"{line}\r\n"
        origin_request += "\r\n"

        origin_socket.sendall(origin_request.encode())

        # Receive response from origin server
        response = b""
        while True:
            part = origin_socket.recv(4096)
            if not part:
                break
            response += part

        # Send the response back to the client
        client_socket.sendall(response)

        # Close the sockets
        origin_socket.close()
        client_socket.close()

    except Exception as e:
        print(f"Error handling request: {e}")
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nError handling request".encode())
        client_socket.close()

# Start the proxy server
def start_proxy():
    """
    Starts the proxy server to accept incoming client connections.
    """
    try:
        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((PROXY_HOST, PROXY_PORT))
        server_socket.listen(5)
        print(f"[*] Proxy Server listening on {PROXY_HOST}:{PROXY_PORT}")

        while True:
            # Accept incoming client connections
            client_socket, addr = server_socket.accept()
            print(f"[*] Connection accepted from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except Exception as e:
        print(f"Error starting proxy server: {e}")

if __name__ == "__main__":
    start_proxy()
