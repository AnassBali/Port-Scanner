from queue import Queue
import socket
import threading
from IPy import IP
import pyfiglet

result = pyfiglet.figlet_format("BAAS")
print(result)

queue = Queue()
open_ports = []


def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((check_ip(target), port))
        sock.sendto("GET / HTTP/1.1\r\n".encode('ascii'), (target, port))
        banner = sock.recv(1024).decode().strip('\n')
        return sock, banner
    except socket.timeout:
        return None, None
    except Exception as e:
        return None, None


def get_ports(mode):
    if mode == 1:
        for port in range(1, 1025):
            queue.put(port)
    elif mode == 2:
        for port in range(1, 48129):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        start = int(input("Enter starting port:"))
        end = int(input("Enter ending port:"))
        for port in range(start, end):
            queue.put(port)
    elif mode == 5:
        ports = input("Enter your ports (separate by space):")
        ports = map(int, ports.split())
        for port in ports:
            queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        sock, banner = portscan(port)
        if sock:
            try:
                print(f"Port {port} is open! Banner: {banner}")
                open_ports.append(port)
                sock.close()
            except Exception as e:
                print(f"Port {port} is open! Failed to get banner.")
                open_ports.append(port)
        else:
            print(f"Port {port} is closed!")


def run_scanner(threads, mode):
    target = input("Enter Target:")
    get_ports(mode)
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    print("Open ports are:", open_ports)


mode = int(input("Enter Mode[1:1-1024, 2:1-48128, 3:Selected Few, 4:Custom(Range), 5:Custom(Specific)]:"))
threads = int(input("Enter the number of threads:"))
run_scanner(threads, mode)
