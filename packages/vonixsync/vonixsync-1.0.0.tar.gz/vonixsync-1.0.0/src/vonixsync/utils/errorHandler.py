import warnings


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    WHITE = "\033[37m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def fxn():
    warnings.warn("deprecated", DeprecationWarning)


def print_finalized(array, column):
    if len(array) == 0:
        return print(
            f"\n{bcolors.OKGREEN}syncronization of {column} table finalized with success\n\n {bcolors.WHITE}"
        )

    if len(array) > 0:
        print(
            f"""                                           
{bcolors.WARNING}Error during insertion:
                    """
        )
        for error in array:
            print(f"{bcolors.WHITE}{error}", end="\n\n\n")

        print(
            f"syncronization of {column} table finalized with {bcolors.WARNING} warning {bcolors.WHITE} \n\n {bcolors.WHITE}"
        )


def ApiKeyError(key, column, id):
    return f"The key {key} was not found in {column} object with id = {id}"
