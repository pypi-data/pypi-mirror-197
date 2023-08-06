from .errorHandler import bcolors


class RequestError(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status

    def __str__(self):
        return f"{bcolors.FAIL}RequestError: {self.message}\nStatus: {self.status}{bcolors.WHITE}"


class DataNull(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return f"{bcolors.WARNING}RequestError: No data found.\n\n\n{bcolors.WHITE}Status: {self.status}\n"


class NullPages(Exception):
    def __init__(self, column):
        self.column = column

    def __str__(self):
        return f"finishing {self.column} syncronization with no changes committed to corresponding table\n{bcolors.WHITE}"


class ConnectionDatabaseError(Exception):
    def __init__(self, array):
        self.array = array

    def print_finalized(self):
        print(f"\n{bcolors.FAIL}Failed to insert:\n")

        for error in self.array:
            print(
                f"{bcolors.WARNING}{error['Database_connection_error']}",
                end=f"\nPlease check your database connection parameters\n\n {bcolors.WHITE}",
            )
