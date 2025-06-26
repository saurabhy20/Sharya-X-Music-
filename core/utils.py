def hacker_text(text: str) -> str:
    RED = "\033[1;31m"
    WHITE = "\033[1;37m"
    RESET = "\033[0m"
    return f"{RED}⚡{WHITE} {text} {RED}⚡{RESET}"
