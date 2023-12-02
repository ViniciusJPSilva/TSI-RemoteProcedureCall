

OPEN_MODE = 'a'
NEW_LINE = '\n'

class Log:
    @staticmethod
    def write(file_name: str, text: str) -> None:
        with open(file_name, OPEN_MODE) as file:
            file.write(f"{text}{NEW_LINE}")