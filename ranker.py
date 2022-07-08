from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from __init__ import *
from math import floor
from pyperclip import copy

console = Console()

def main():
    """Implements a way to rank any arbitrary item"""
    ranker = Ranker()
    # Set up a way to let the user leave the program
    try:
        ranker.run()

    except KeyboardInterrupt:
        console.print("\nGood bye", style="#ffff00")

def add_item(finlist) -> None:
    """Adds an item based on the user input"""
    item_name    = console.input("Name of item: ")
    item_ranking = ""
    while not(is_float(item_ranking)):
        item_ranking = console.input("Rank: ")
        if not(is_float(item_ranking)):
            console.print("Please enter a", end=' ')
            console.print("number", style="#ff0000 bold italic")
    item_ranking = floor(float(item_ranking))
    finlist.insert(item_ranking, item_name)

def delete_item(finlist) -> None:
    """Deletes an item based on the user input"""
    item_index: str = request_int("Which item would you like to delete?")
    value = finlist[item_index]
    if Confirm.ask(f"Deleting [white bold]{value}[/]. Continue?"):
        finlist.pop(item_index)

def rename_item(finlist) -> None:
    """Renames an item based on the user input"""
    item_index = request_int("Which item would you like to edit?")

    console.print("Item chosen:", end=' ')
    console.print(finlist[item_index], style="white bold")
    new_name = console.input("Enter the new name of the value: ")

    finlist[item_index] = new_name

def move_item(finlist) -> None:
    """Changes the position of an item based on the user input"""
    message: str = "Which item do you want to move?"
    item_index: int = request_int(message)
    message = "Choose the number you want to move it to"
    moving_index: int = request_int(message)

    initial_item = finlist.pop(item_index)
    finlist.insert(moving_index, initial_item)

def copy_rankings(finlist) -> None:
    """Copies the rankings to the system clipboard"""
    finstr = as_str()
    copy(finstr)
    console.print("[#00ff00]Copied:[/]", finstr)

def as_str() -> str:
    """Returns the currently available rankings as a string"""
    finstr = ""
    for index, element in enumerate(finlist):
        finstr += f"{index+1}. {element}\n"
    return finstr

def export_txt(finlist) -> None:
    """Exports the rankings to a text file"""
    finstr = as_str()
    write_to_file("Name of file: ", ".txt", finstr)

def write_to_file(prompt: str, extension: str, data: str) -> None:
    """Exports the given string to a file, named based on the user input"""
    console.print(prompt, style="#ffff00 bold", end='')
    file_name = input() + extension
    with open(file_name, 'w') as my_file:
        my_file.write(data)
    console.print(f"[#ffff00 bold]Exported to:[/] [white b]{file_name}[/]")

def export_csv(finlist) -> None:
    HEADER = "Item,Rank\n"

    data = ""
    for index, value in enumerate(finlist):
        data += f"{value},{index+1}\n"

    csv = HEADER + data
    write_to_file("Name of file: ", ".csv", csv)

def request_int(message) -> int:
    console.print(message)

    item_number_input = ""
    while (not(item_number_input.isnumeric())):
        item_number_input = console.input("Enter [i]number[/]: ")
        if (not(item_number_input.isnumeric())):
            console.print("Please enter a", end=' ')
            console.print("whole number", style="#ff0000 bold italic")
    
    return int(item_number_input)-1

def get_table(finlist: list) -> Table:
    table = Table(title="Ranker", header_style="#ff8a65 bold")
    for i in ["Item", "Ranking"]:
        table.add_column(i)

    count = 1
    for i in finlist:
        table.add_row(i, str(count))
        count += 1

    return table

class Ranker:
    __empty: dict = {
        "Create new list" : add_item
    }

    __non_empty : dict = {
        "Modify List" : {
            "Add a new item" : add_item,
            "Delete a item"  : delete_item,
            "Rename an item" : rename_item,
            "Move Item"      : move_item
        },
        "Export" : {
            "Copy to clipboard"   : copy_rankings,
            "Export as .txt file" : export_txt,
            "Export as .csv file" : export_csv
        }
    }

    def __init__(self):
        # For storing the data of the rankings
        self.__finlist = []

        # For showing available options
        self.__root: dict = Ranker.__empty
        self.__current_options = list(Ranker.__empty)
        # Works in conjunction with self.__current_options. Used to navigate
        # through the current options for the user
        self.__path = []

        # Depending on whether self.__finlist is empty or not, the available
        # options will be different for the user
        self.__has_items = False

    def __get_options_list(self, options: dict) -> list:
        empty_path: bool = self.__path == []
        if empty_path:
            return list(options)

        # We do not want to unintentionally modify the options dictionary 
        try:
            from copy import copy as cp
        except ImportError:
            pass

        # Traverse through the path to get to the final destination within the
        # dictionary
        final_options: dict = cp(options)
        for i in self.__path:
            final_options = final_options[i]
        return final_options

    def run(self):
        """Runs the Ranker class"""
        # We don't need to print the table if it is the root element
        self.__has_items = len(self.__finlist) != 0
        is_nonempty_root = self.__has_items and len(self.__path) == 0
        if (is_nonempty_root):
            console.print(get_table(self.__finlist))
            options = self.__get_options_list(Ranker.__non_empty)
        else:
            options = ["Add a new item"]

        # User input is required to know what the program should do
        choice = Prompt.ask_options(
            question = "What would you like to do?",
            options = options
        )

        # Prevent the impossible
        assert(0 < choice <= len(options))

        self.__parse_choices(choice)
        self.run()

    def __parse_choices(self, choice: int):
        if len(self.__path) == 0:
            pass
        {
            1 : add_item,
            2 : delete_item,
            3 : rename_item,
            4 : move_item,
            5 : copy_rankings,
            6 : export_txt,
            7 : export_csv
        }[choice](self.__finlist)

if __name__ == "__main__":
    main()

