import socket  # Importing the socket module to work with network connections
import threading  # Importing the threading module to handle concurrent client connections

# Define the proxy server address and port
PROXY_HOST = 'localhost'  # Host address where the proxy server will listen (localhost for local testing)
PROXY_PORT = 8080  # Port number where the proxy server will listen

# Function to handle client connections
def handle_client(client_socket):
    """
    This function handles incoming client connections. It receives the request from the client,
    processes it (for now, it just prints the request), and sends a placeholder response back to the client.
    """
    # Receive the client's request (up to 4096 bytes) and decode it to a string
    request = client_socket.recv(4096).decode()
    print("Received request:\n", request)
    
    # Placeholder HTTP response. For now, it just sends back a simple 200 OK response with a short message
    response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, Proxy!"
    # Send the response to the client
    client_socket.sendall(response.encode())
    # Close the connection with the client
    client_socket.close()

# Start the proxy server
def start_proxy():
    """
    This function sets up the proxy server. It creates a listening socket that waits for incoming connections.
    When a connection is received, it handles the connection in a separate thread to allow multiple clients 
    to be processed simultaneously.
    """
    # Create a TCP socket using IPv4 address family (AF_INET) and SOCK_STREAM type (TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified host and port (localhost and port 8080)
    server_socket.bind((PROXY_HOST, PROXY_PORT))
    
    # Start listening for incoming connections, with a maximum backlog of 5 (number of clients to queue)
    server_socket.listen(5)
    print(f"[*] Proxy Server listening on {PROXY_HOST}:{PROXY_PORT}")
    
    # Continuously accept incoming connections and handle them
    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        # Print out the address of the client that connected
        print(f"[*] Connection accepted from {addr}")
        
        # For each client connection, spawn a new thread to handle the client request independently
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Check if the script is being run directly (and not imported as a module)
if __name__ == "__main__":
    # Start the proxy server by calling the start_proxy function
    start_proxy()
