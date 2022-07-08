from typing import List
from rich.console import Console

console = Console()

def is_float(value: int) -> bool:
    """Checks if the given value is a float"""
    try:
      float(value)
      return True
    except ValueError:
      return False

def path_print(path = str, separator='/') -> None:
    """
    Prints the path so that it is intuitively understood which directory is
    the leaf directory
    """
    pathlist = path.split(separator)
    style = Palette.GREY + ' ' + Palette.BOLD
    for i in pathlist[:-1]:
        console.print(i + separator, end='', style=style)
    style = Palette.WHITE + ' ' + Palette.BOLD
    console.print(pathlist[-1], style=Palette.WHITE)

class Prompt:
    @staticmethod
    def ask_options(question: str, options: List[str]) -> int:
        question_style = "bold white"
        console.print(question, style=question_style)
        for i in range(1, len(options)+1):
            option_number_style = "bold #fff176" # yellow
            console.print(i, style=option_number_style, end=' ')
            console.print(options[i-1])

        choice: str = ""
        while not(choice.isnumeric()):
            console.print("Enter a [b i white]number[/]: ", end='')
            choice = input()
            if not(choice.isnumeric()):
                console.print("Error", style="#e53935 bold") # red
                console.print("Not a number.\nPlease enter a [i]number[/]")
        return int(choice)

class Palette:
    GREY:  str = "#888888"
    WHITE: str = "white"
    BOLD:  str = "bold"

def traverse(options: dict, path: list):
    """
    Moves through the list to print out the current option the 
    user is in.
    """

