# CNA-Assignment1
Programming Assignment 1: HTTP Web Proxy Server Programming Assignment (Python based 2025)
# Proxy Server

This is a simple proxy server implemented in Python that listens for incoming client connections, processes requests, and sends back placeholder responses. The server uses sockets and threading to handle multiple client connections concurrently.

## Features

- Listens on `localhost` at port `8080` (can be changed by modifying the `PROXY_HOST` and `PROXY_PORT` variables).
- Handles incoming client requests by spawning a new thread for each connection, allowing for concurrent connections.
- Sends a basic placeholder HTTP response back to the client.

## How It Works

1. The proxy server listens on a specified host and port (default: `localhost:8080`).
2. When a client connects, it sends a request to the proxy server.
3. The server receives and prints the request, then sends back a simple `200 OK` HTTP response with a content message of "Hello, Proxy!".
4. The server uses threading to handle multiple client connections simultaneously.

