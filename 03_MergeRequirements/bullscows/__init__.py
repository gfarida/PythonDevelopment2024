import random
import cowsay
from pathlib import Path

def bullscows(guess: str, secret: str) -> (int, int):
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(min(guess.count(c), secret.count(c)) for c in set(guess))
    return bulls, cows - bulls

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempts = 0
    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, secret_word)
        if bulls == len(secret_word):
            return attempts
        inform("Быки: {}, Коровы: {}", bulls, cows)

def ask(prompt: str, valid: list[str] = None) -> str:
    user_input = input(prompt).strip().lower()
    cow = Path(__file__).parent / "fox_winking"
    if valid is not None:
        while user_input not in valid:
            print(cowsay.cowsay("Недопустимое слово!", cow=cow))
            user_input = ask(prompt, valid)
    return user_input
        

def inform(format_string: str, bulls: int, cows: int) -> None:
    cow = Path(__file__).parent / "fox_winking"
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=cow))