# coding: utf-8
from colorama import Fore, Back, Style
from .colors import Colors


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
