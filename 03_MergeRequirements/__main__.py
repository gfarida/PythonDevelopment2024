import sys
import urllib.request

from bullscows import ask, gameplay, inform

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m bullscows dictionary [length]")
        sys.exit(1)

    dictionary = sys.argv[1]
    word_length = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    if dictionary.startswith("http"):
        response = urllib.request.urlopen(dictionary)
        words = [word.decode().strip() for word in response.readlines()]
    else:
        with open(dictionary, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if len(line.strip()) == word_length]

    attempts = gameplay(ask, inform, words)
    print("Количество попыток:", attempts)


if __name__ == "__main__":
    main()
