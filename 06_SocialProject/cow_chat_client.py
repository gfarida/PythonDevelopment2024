import cmd
import threading
import time
import readline
import socket
import shlex

dict = {}
class CmdClient(cmd.Cmd):

    def __init__(self, socket):
        super().__init__()
        self.s = socket
        self.msg_num = 0
        self.compl = None

    def do_login(self, cowname):
        self.s.send(f"login {cowname}\n".encode())
    
    def do_who(self, arg):
        self.s.send("who\n".encode())
    
    def do_cows(self, arg):
        self.s.send("cows\n".encode())
    
    def do_quit(self, arg):
        self.on = False
        if self.is_login:
            self.s.send("quit\n".encode())
        else:
            self.sock.shutdown(socket.SHUT_WR)
        exit(0)
    
    def do_yield(self, arg):
        self.s.send(f"yield {arg}\n".encode())
    
    def do_say(self, arg):
        arg_list = self.parse_shlex(arg)
        self.s.send(f"say {arg_list[0]} {arg_list[1]}\n".encode())
    
    def complete_login(self, text, line, begidx, endidx):
        args = shlex.split(text)
        start = []
        if len(args) == 1:
            start = args[-1]
        elif line[-1] == " ":
            start = None
        else: 
            return start
        
        self.s.send(f"cows {self.msg_num}\n".encode())
        dict[self.msg_num] = None

        while not dict[self.msg_num]:
            pass
    
        DICT = dict[self.msg_num]

        self.msg_num += 1
        if start is not None:
            return [cow for cow in DICT if cow.startswith(start)]
        else:
            return DICT
    
    def complete_say(self, text, line, begidx, endidx):
        args = shlex.split(text)
        start = []
        if len(args) == 1:
            start = args[-1]
        elif line[-1] == " ":
            start = None
        else: 
            return start
        
        self.s.send(f"who {self.msg_num}\n".encode())
        dict[self.msg_num] = None

        while not dict[self.msg_num]:
            pass
    
        DICT = dict[self.msg_num]

        self.msg_num += 1
        if start is not None:
            return [cow for cow in DICT if cow.startswith(start)]
        else:
            return DICT

    def receive_in_client(self):
        while True:
            answ = socket.recv(1024).decode()
            
            if answ.startswith("***"):
                msg_num, tip = answ.split()[1], answ.split()[2:]
                dict[int(msg_num)] = tip.split(",")
            else:
                print(f"{answ}\n{self.prompt} {readline.get_line_buffer()}", end="", flush=True)

            if not answ:
                break


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 1337))
        cmdline = CmdClient(s)
        timer = threading.Thread(target=cmdline.receive_in_client, args=())
        timer.start()
        cmdline.cmdloop()