import cmd
import shlex
import cowsay

EYES = ['oo', 'OO', '00']
TONGUE = ['U', 'WW', 'J', 'gg']

class CowCmd(cmd.Cmd):
    prompt = "cmd>> "

    def do_list_cows(self, args):
        """List of available cows
           Usage: list_cows """
        print("Cows:", end=' ')
        print(", ".join(cowsay.list_cows()))

    def do_cowsay(self, args):
        """
        Make the cow say something
        Usage: cowsay message [cow] [eyes] [tongue]
        """
        try:
            args = shlex.split(args)
            
            if len(args) < 1 or len(args) > 4:
                print("message argument is required")
                return

            cow = args[1] if len(args) > 1 else 'default'
            eyes = args[2] if len(args) > 2 else "oo"
            tongue = args[3] if len(args) > 3 else "U"
            print(cowsay.cowsay(args[0], cow=cow, eyes=eyes, tongue=tongue))
        except ValueError as e:
            print("Error:", e)
    
    def do_cowthink(self, args):
        """
        Make the cow think something
        Usage: cowthink message [cow] [eyes] [tongue]
        """
        try:
            args = shlex.split(args)

            if len(args) < 1 or len(args) > 4:
                print("message argument is required")
                return

            cow = args[1] if len(args) > 1 else 'default'
            eyes = args[2] if len(args) > 2 else "oo"
            tongue = args[3] if len(args) > 3 else "U"
            print(cowsay.cowthink(args[0], cow=cow, eyes=eyes, tongue=tongue))
        except ValueError as e:
            print("Error:", e)
    
    def complete_cowsay(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        DICT = []

        if len(words) == 3:
            DICT = cowsay.list_cows()
        if len(words) == 4:
            DICT = EYES
        if len(words) == 5:
            DICT = TONGUE
        return [c for c in DICT if c.startswith(text)]
    
    def complete_cowthink(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        DICT = []

        if len(words) == 3:
            DICT = cowsay.list_cows()
        if len(words) == 4:
            DICT = EYES
        if len(words) == 5:
            DICT = TONGUE
        return [c for c in DICT if c.startswith(text)]

    def do_quit(self, args):
        """Exit the program"""
        print("Quitting...")
        return True


if __name__ == "__main__":
    CowCmd().cmdloop()
