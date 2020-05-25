import select
import socket
import threading
import datetime

from recorder import Recorder


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket, raw):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.raw = raw
        self.recorder = Recorder("../record/" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".eeg")
        self.client_address = client_address
        print ("New connection added: ", self.client_address)

    def run(self):
        print ("Connection from : ", self.client_address)

        self.client_socket.setblocking(0)
        data_to_parse = ""

        while True:
            ready = select.select([self.client_socket], [], [], 10)
            if ready[0]:
                data = self.client_socket.recv(2048)
                # print ">" + data
                data_to_parse += data
                if len(data) == 0:
                    self.client_socket.close()
                    break
                if data_to_parse[-1] == 'X':
                    x = data_to_parse.split('X')
                    data_to_parse = ''
                else:
                    x = data_to_parse.split('X')
                    data_to_parse = x.pop()
                for f in x:
                    if len(f) > 0:
                        # print "-- " + f
                        # if f[0] == 'A':
                        #     print str(a_state) + "=>" + f
                        #     if a_state == 0:
                        #         self.client_socket.send('0')
                        #     if a_state == 1:
                        #         self.client_socket.send('1')
                        #     if a_state == 2:
                        #         self.client_socket.send('2')
                        #     if a_state == 3:
                        #         self.client_socket.send('3')
                        #     if a_state == 4:
                        #         self.client_socket.send('4')
                        if f[0] == 'P':
                            print "=>" + f
                            self.client_socket.send(f + 'X')
                        elif f[0] == 'D':
                            val_str = f[1:].split(',')
                            try:
                                val = [float(i) for i in val_str]
                            except ValueError:
                                # TO fix!!!!
                                val = [0.0, 0.0, 0.0, 0.0]
                            self.raw.add_float(val)
                            if self.recorder:
                                self.recorder.add_float(val)
            else:
                self.client_socket.close()
                break
        print ("Client at ", self.client_address, " disconnected...")
        if self.recorder:
            self.recorder.close()


class Server:
    def __init__(self, raw):
        host = "0.0.0.0"
        port = 6543
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        print("Server started")
        print("Waiting for client request..")

        while True:
            server.listen(1)
            client_sock, client_address = server.accept()
            new_thread = ClientThread(client_address, client_sock, raw)
            new_thread.start()
