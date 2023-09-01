from colorama import Fore, Back, Style


class Colors:
    @staticmethod
    def result(text, is_ok=True):
        if is_ok:
            text = Fore.LIGHTGREEN_EX + str(text) + Fore.RESET
            return " [" + Colors.green(text) + "]"
        else:
            text = Fore.LIGHTRED_EX + str(text) + Fore.RESET
            return " [" + Colors.red(text) + "]"
        pass

    @staticmethod
    def green(text):
        return Fore.LIGHTGREEN_EX + str(text) + Fore.RESET

    @staticmethod
    def red(text):
        return Fore.LIGHTRED_EX + str(text) + Fore.RESET

    @staticmethod
    def blue(text):
        return Fore.LIGHTBLUE_EX + str(text) + Fore.RESET

    @staticmethod
    def yellow(text):
        return Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET

    @staticmethod
    def magenta(text):
        return Fore.LIGHTMAGENTA_EX + str(text) + Fore.RESET
