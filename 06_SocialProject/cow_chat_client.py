import cmd
import threading
import time
import readline
import socket
import shlex


class CmdClient(cmd.Cmd):

    def __init__(self, socket):
        super().__init__()
        self.s = socket
        self.on = True
        self.is_login = False
        self.compl = None

    def do_login(self, cowname):
        self.s.send(f"login {cowname}\n".encode())
    
    def do_who(self):
        self.s.send("who\n".encode())
    
    def do_cows(self):
        self.s.send("cows\n".encode())
    
    def do_quit(self):
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
        words = (line[:endidx]).split()
        self.s.send("complete_cows\n".encode())

        while self.compl is None:
            pass

        compls = [line.strip() for line in self.compls.split()[1:]]
        if words[-1] != "login":
            compls = [line for line in compls if line.startswith(words[-1])]
            if len(compls) == 0:
                compls = None
        self.compls = None
        return compls
    
    def complete_say(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()
        self.s.send("complete_who\n".encode())
        while self.compl is None:
            pass

        compls = [line.strip() for line in self.compls.split()[1:]]
        if words[-1] != "say":
            compls = [line for line in compls if line.startswith(words[-1])]
            if len(compls) == 0:
                compls = None
        self.compls = None
        return compls

    def receive_in_client(self):
        while True:
            if not self.on:
                break 
            get_data = self.sock.recv(1024).decode()

            if get_data.startswith("compl"):
                self.completion = get_data
            elif get_data.startswith("quit"):
                break
            elif get_data.strip().startswith("Empty message"):
                pass
            else:
                if get_data.strip().startswith(
                    "You've logged in succesfully with cow name:"
                ):
                    self.logged = True
                print(
                    f"\n{get_data.strip()}\n{self.prompt}{readline.get_line_buffer()}",
                    end="",
                    flush=True,
                )    


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 1337))
        cmdline = CmdClient(s)
        timer = threading.Thread(target=cmdline.receive_in_client, args=())
        timer.start()
        cmdline.cmdloop()