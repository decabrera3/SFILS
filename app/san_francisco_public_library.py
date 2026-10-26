
import mysql.connector

RESET_COLOR = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

SHOW_TABLES = "0"

config = {
        "user" : "root",
        "password" : "MyFunP@ssw0rd",
        "host" : "127.0.0.1",
        "database" : "san_francisco_public_library"
        }
connection = mysql.connector.connect(**config)

def print_help():
    print("Command | Description")
    print("      " + CYAN + SHOW_TABLES + RESET_COLOR + " | Shows all the tables in the database.")

def execute_operation(operation):

    if (operation == "exit"):
        return False
    elif (operation == "help"):
        print_help()
    elif(operation == SHOW_TABLES):
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")

        print("\nTables in this database:")
        for table in cursor.fetchall():
            print(table[0])
    else:
        print(RED + "Invalid Command" + RESET_COLOR)

    return True


is_running = True
while (is_running):
    operation = input("\nWhat would you like to do?\n>> " + YELLOW).casefold()
    print(RESET_COLOR, end="")
    is_running = execute_operation(operation)


connection.close()