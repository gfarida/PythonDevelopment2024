import cmd
import shlex
import cowsay

class CowCmd(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to CowCmd! Type help or ? to list commands.\n"

    def do_list_cows(self, args):
        """List available cows."""
        print("Available cows:")
        print(", ".join(cowsay.list_cows()))

    def do_make_bubble(self, args):
        """Make a bubble."""
        print("Making a bubble...")

    def do_cowsay(self, args):
        """Make the cow say something."""
        try:
            args = shlex.split(args)
            message = args[0] if args else "Hello"
            cow = args[1] if len(args) > 1 else None
            eyes = args[2] if len(args) > 2 else "oo"
            tongue = args[3] if len(args) > 3 else "  "
            print(cowsay.cowsay(message, cow=cow, eyes=eyes, tongue=tongue))
        except ValueError as e:
            print("Error:", e)

    def do_cowthink(self, args):
        """Make the cow think something."""
        try:
            args = shlex.split(args)
            message = args[0] if args else "Hmm..."
            cow = args[1] if len(args) > 1 else None
            eyes = args[2] if len(args) > 2 else "oo"
            tongue = args[3] if len(args) > 3 else "  "
            print(cowsay.cowthink(message, cow=cow, eyes=eyes, tongue=tongue))
        except ValueError as e:
            print("Error:", e)

    def do_quit(self, args):
        """Exit the program."""
        print("Quitting...")
        return True

    def help_quit(self):
        print("Exit the program.")

if __name__ == "__main__":
    CowCmd().cmdloop()
