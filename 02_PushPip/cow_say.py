import argparse
import cowsay

def main():
    parser = argparse.ArgumentParser(description='Python implementation of cowsay')
    parser.add_argument('message', nargs='?', help='Message to display (default is "Hello")')
    parser.add_argument('-f', '--file', metavar='cowfile', default='default', help='Specify the cowfile to use')
    parser.add_argument('-e', '--eyes', metavar='eye_string', default='oo', help='Change the cow\'s eyes')
    parser.add_argument('-T', '--tongue', metavar='tongue_string',  default='  ', help='Change the cow\'s tongue')
    parser.add_argument('-W', '--width', metavar='wrapcolumn', type=int,  default=40, help='Specify line width')
    parser.add_argument('-l', '--list', action='store_true', help='List available cowfiles')
    parser.add_argument('-b', '--borg', action='store_true', help='Borg mode')
    parser.add_argument('-d', '--dead', action='store_true', help='Make the cow appear dead')
    parser.add_argument('-g', '--greedy', action='store_true', help='Invoke greedy mode')
    parser.add_argument('-p', '--paranoid', action='store_true', help='Cause a state of paranoia')
    parser.add_argument('-s', '--stoned', action='store_true', help='Make the cow appear stoned')
    parser.add_argument('-t', '--tired', action='store_true', help='Yields a tired cow')
    parser.add_argument('-w', '--wired', action='store_true', help='Initiates wired mode')
    parser.add_argument('-y', '--youthful', action='store_true', help='Brings on the cow\'s youthful appearance')
    parser.add_argument('-n', '--nowrap', action='store_true', help='Disable word wrap (-n)')
    args = parser.parse_args()

    if args.list:
        print(cowsay.list_cows())
        return
    
    cowfile = None
    if args.file != 'default':
        cowfile = cowsay.get_cow(args.file)

    message = args.message if args.message else "Hello"
    mode = ''
    if args.dead:
        mode = 'd'
    elif args.greedy:
        mode = 'g'
    elif args.paranoid:
        mode = 'p'
    elif args.stoned:
        mode = 's'
    elif args.tired:
        mode = 't'
    elif args.wired:
        mode = 'w'
    elif args.youthful:
        mode = 'y'
    
    if cowfile is None:
        cow_arg = args.file
    else:
        cow_arg = None
    
    if not args.nowrap:
        print(cowsay.cowsay(message, cow=cow_arg, eyes=args.eyes, tongue=args.tongue, width=args.width, preset=mode, cowfile=cowfile))
    else:
        print(message)

if __name__ == '__main__':
    main()