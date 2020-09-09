import sys, textwrap, socketserver, string, readline, threading
from time import *
import getpass, os, subprocess
from pwn import *
from random import randrange
import json

class Service(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            command = self.receive('Cmd: ').decode("utf-8")
            #p = subprocess.Popen(command,
            #  shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            #self.send(p.stdout.read())
            if command != "":
                to_send=command.split(",")
                recive_message(myself,neighbors,to_send[1],to_send[0])

    def send(self, string, newline=True):
        if newline:
            string = str(string) + '\n'
        try:
            self.request.sendall(bytes(string, 'utf-8'))
        except:
            pass

    def receive(self, prompt='> '):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass

###########################################################
def get_neighbors(neighbors):
    return list(neighbors.keys())

def is_neighbor(neighbors,destination):
    if destination in get_neighbors(neighbors):
        return True
    return False

def is_destination(myself,destination):
    if myself == destination:
        return True
    return False

def send_message(neighbors,destination, msg="test"):
    if is_neighbor(neighbors,destination):
        print("Si es vecino :D")
        print("Enviando paquete a",destination,"con IP:",neighbors[destination][0])
        conn = remote(neighbors[destination][0], neighbors[destination][1])
        conn.send(msg+","+destination)
        conn.close()
    else:
        print("Pues no es su vecino :c")
        n_neighbors=len(get_neighbors(neighbors))
        #print(list(get_neighbors(neighbors)))
        forward = get_neighbors(neighbors)[randrange(n_neighbors)]
        print("Se eligió a",forward, "con IP", neighbors[forward][0], "Pero el destinatario sigue siendo", destination)
        conn = remote(neighbors[forward][0], neighbors[forward][1])
        conn.send(msg+","+destination)
        conn.close()

def recive_message(myself,neighbors,destination,msg="test"):
    if is_destination(myself,destination):
        #print("Yo soy, recibido manito uwu")
        print("-"*20)
        print("Mensaje recibido")
        print("-"*20)
        print("| "+msg)
        print("-"*20)
    else:
        print("No soy yo, enviando mensaje a otro")
        send_message(neighbors,destination,msg)

def import_profile(file):

    neighbors_t={}

    f = open(file[:-1]+".pf", "r")
    linea = f.read()
    result = json.loads(linea, strict=False)

    myself_t = result["myself"]
    port_t = int(result["port"])

    name_n = list(result["neighbors"].keys())
    for i in name_n:
        neighbors_t[i]=tuple(result["neighbors"][i])

    return myself_t,neighbors_t,port_t

###########################################################

def main():
    global myself,neighbors
    file=input("Enter file profile: ")
    myself,neighbors,port = import_profile(file)

    host = '0.0.0.0'
    print('Starting server...')
    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=(server.serve_forever))
    server_thread.daemon = True
    server_thread.start()
    print('Server started on ' + str(server.server_address) + '!')

    print("I am",myself)

    for i in neighbors.keys():
        print("My neighbor is", i)

    while True:
        print("-"*20)
        print("¿Que desea hacer?")
        print("1) Enviar Un mensaje")
        print("0) Exit")
        r=input("> ")[:-1]
        if r == '1':
            dst=input("Para quien?: ")[:-1]
            txt=input("Que le quieres decir?: ")[:-1]
            send_message(neighbors,dst, msg=txt)
        elif r == '0':
            break


if __name__ == '__main__':
    main()