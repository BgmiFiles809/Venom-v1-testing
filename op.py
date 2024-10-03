import socket

def capture_udp_packets(host='0.0.0.0', port=12345):
    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    sock.bind((host, port))

    print(f"Listening for UDP packets on {host}:{port}...")

    while True:
        packet, addr = sock.recvfrom(65535)  # Buffer size is 65535 bytes
        print(f"Received packet from {addr}: {packet}")

if __name__ == "__main__":
    capture_udp_packets()