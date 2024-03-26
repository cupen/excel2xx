# coding: utf-8
import colorama
from colorama import Fore

# from .colors import Colors
colorama.init(autoreset=True)


def info(text):
    print(Fore.LIGHTCYAN_EX + str(text) + Fore.RESET)


def warn(text):
    print(Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET)


def error(text):
    print(Fore.LIGHTRED_EX + str(text) + Fore.RESET)


def success(text):
    text = Fore.LIGHTGREEN_EX + str(text) + Fore.RESET
    print(f"[{text}]")


def fail(text):
    text = Fore.LIGHTRED_EX + str(text) + Fore.RESET
    print(f"[{text}]")
