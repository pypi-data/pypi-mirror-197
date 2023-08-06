"""This is  the "Nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""

def print_lol(the_list):
    """This function takes one positional argument "called list"? which in the Python
     list (of-possibly-nested lists). \each data item in the provided list is (recursively) printed to
     the screen"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)