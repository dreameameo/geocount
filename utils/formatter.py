try:
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class EmptyColor:
        def __getattr__(self, name):
            return ""
    Fore = Style = EmptyColor()

def print_header(title):
    print(Fore.CYAN + Style.BRIGHT + "\\n" + "=" * 55)
    print(title.center(55))
    print("=" * 55 + Style.RESET_ALL)

def print_message(message, level="info"):
    color = {"success": Fore.GREEN, "warning": Fore.YELLOW,
             "error": Fore.RED, "info": Fore.CYAN}.get(level, "")
    print(color + message + Style.RESET_ALL)

def pause():
    input("\nTekan Enter untuk kembali ke menu...")