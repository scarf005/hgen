from dataclasses import dataclass

@dataclass(frozen=True)
class Color:
    red = "\033[91m"
    green = "\033[92m"
    blue = "\033[94m"
    cyan = "\033[96m"
    white = "\033[97m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    grey = "\033[90m"
    black = "\033[90m"
    default = "\033[99m"
    end = "\033[0m"

    @classmethod
    def cstr(cls, color: str, string: str):
        return f"{getattr(cls, color)}{string}{Color.end}"

    @classmethod
    def cprint(cls, color: str, string: str):
        print(cls.cstr(color, string))