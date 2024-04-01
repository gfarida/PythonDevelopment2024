import cmd
import threading
import time
import readline
import socket


class CmdClient(cmd.Cmd):

    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def do_login(self, user):
        self.s.send(f"login {user}\n".encode())
    
    def do_who(self):
        self.s.send("who\n".encode())
    
    def do_cows(self):
        self.s.send("cows\n".encode())
    
    def do_quit(self):
        self.s.send("quit\n".encode())
        exit(0)
    
    def do_yield(self, arg):
        self.s.send(f"yield {arg}\n".encode())
    
    def do_say(self, arg):
        arg_list = self.parse_shlex(arg)
        self.request(f"say {arg_list[0]} {arg_list[1]}\n".encode())
    
    def complete_login(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()
        self.request("complete_cows")
    


    def receive_in_client(self):
        while True:


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 1337))
        cmdline = CmdClient(s)
        timer = threading.Thread(target=cmdline.receive_in_client, args=())
        timer.start()
        cmdline.cmdloop()